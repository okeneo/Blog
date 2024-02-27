from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.urls import reverse_lazy

from .models import (
    UserProfile,
    VerificationEmailToken,
    VerificationEmailUpdateToken,
    VerificationPasswordResetToken,
)
from .tasks import send_verification_email_task

EMAIL_TEMPLATES = {
    "registration": {
        "subject": "Verify your email address",
        "message": "Follow this link to verify your account.",
        "url_name": "blog:verify_email",
    },
    "update_email": {
        "subject": "Email Update Verification",
        "message": "If you didn't change it, you should click this link to recover it.",
        "url_name": "blog:verify-email-update",
    },
    "reset_password": {
        "subject": "Reset Password",
        "message": "If you didn't change it, you should click this link to recover it.",
        "url_name": "blog:verify-password-reset",
    },
}


def send_verification_email(template_type, email, token_key):
    """Send a verification email based on the specified template.

    Args:
        template_type (str): Type of email template.
        email (str): Recipient's email address.
        token_key (str): Unique token key for email verification.
    """
    template = EMAIL_TEMPLATES.get(template_type)
    if not template:
        raise ValueError(f"Unsupported email template: {template}.")

    # Get email url.
    url_name = template["url_name"]
    url = reverse_lazy(url_name)
    HOST = settings.HOST
    email_url = f"{HOST}{url}?token_key={token_key}"

    # Collect email subject and message.
    template_message = template["message"]
    message = f"{template_message}\n{email_url}"
    subject = template["subject"]

    # Pass email sending to celery.
    send_verification_email_task.delay(subject, message, email)


def validate_email_token_key(token_key):
    try:
        token = VerificationEmailToken.objects.get(key=token_key)
    except VerificationEmailToken.DoesNotExist:
        raise ValidationError("Invalid verification token.")

    if token.is_expired:
        raise ValidationError("Token expired.")

    return token


def validate_email_update_token_key(token_key):
    try:
        token = VerificationEmailUpdateToken.objects.get(key=token_key)
    except VerificationEmailUpdateToken.DoesNotExist:
        raise ValidationError("Invalid verification token.")

    if token.is_expired:
        raise ValidationError("Token expired.")

    return token


def validate_reset_password_token_key(token_key):
    try:
        token = VerificationPasswordResetToken.objects.get(key=token_key)
    except VerificationPasswordResetToken.DoesNotExist:
        raise ValidationError("Invalid verification token.")

    if token.is_expired:
        raise ValidationError("Token expired.")

    return token


def validate_resend_verification_email_operation(email):
    """Given an unverified email, validate that the user should be resent a new
    verification email."""
    if not email:
        raise ValidationError("Email Required.")

    try:
        user = UserProfile.objects.get(email=email)
    except UserProfile.DoesNotExist:
        raise ValidationError("User not found.")

    if user.is_active:
        raise ValidationError("User already registered.")

    try:
        token = VerificationEmailToken.objects.get(user=user)
    except VerificationEmailToken.DoesNotExist:
        # A scenario where an inactive user tries to access this endpoint.
        # This is equivalent to not user.is_active and not user.is_email_verified because
        # there should always be a token for a user that is not active but are yet to
        # verify their email.
        raise ValidationError("Unauthorized access.")

    if token.has_exceeded_maximum_attempts:
        raise ValidationError("Exceeded maximum send attempts.")

    return token, user


def validate_new_email(new_email, user):
    MAX_LENGTH = 255

    if not new_email:
        raise ValidationError("New email required.")

    new_email = clean_email(new_email)

    if len(new_email) > MAX_LENGTH:
        raise ValidationError("The new email address is too long.")

    try:
        validate_email(new_email)
    except ValidationError as e:
        raise ValidationError(str(e))

    if user.email == new_email:
        raise ValidationError(
            "The new email address must be different from the current email address."
        )

    try:
        UserProfile.objects.get(email=new_email)
        raise ValidationError(f"The email address '{new_email}' is already registered.")
    except UserProfile.DoesNotExist:
        return new_email


def clean_email(email):
    cleaned_email = email.lstrip("\n\r ").rstrip("\n\r ")
    cleaned_email = cleaned_email.lower()
    return cleaned_email


def get_sentinel_user():
    return UserProfile.objects.get(username="deleted")


def handle_deleted_user_comments(user):
    leaf_comments = user.comments.filter(parent_comment__isnull=False)
    leaf_comments.delete()
    parent_comments = user.comments.filter(parent_comment__isnull=True)
    parent_comments.update(user=get_sentinel_user(), is_deleted=True, text="")

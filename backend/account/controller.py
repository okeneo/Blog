from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email

from .models import (
    UserProfile,
    VerificationEmailToken,
    VerificationEmailUpdateToken,
    VerificationResetPasswordToken,
)

# from django.urls import reverse
# verification_url = reverse("email_confimation")
EMAIL_TEMPLATES = {
    "registration": {
        "subject": "Verify your email address",
        "message": "http://localhost:8000/blog/verify-email/?token_key={token_key}",
    },
    "update_email": {
        "subject": "Email Update Verification",
        "message": "http://localhost:8000/blog/verify-email-update/?token_key={token_key}"
        + "\nIf you didn't change it, you should click this link to recover it.",
    },
    "reset_password": {
        "subject": "Reset Password",
        "message": "http://localhost:8000/blog/verify-reset-password/?token_key={token_key}"
        + "\nIf you didn't change it, you should click this link to recover it.",
    },
}


def send_verification_email(template, email, token_key):
    template = EMAIL_TEMPLATES.get(template)

    if template:
        subject = template["subject"]
        message = template["message"].format(token_key=token_key)
        # Send emails asynchronously?
        send_mail(
            subject=subject,
            message=message,
            from_email=None,
            recipient_list=[email],
            fail_silently=True,
        )
    else:
        raise ValueError(f"Unsupported email template: {template}.")


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
        token = VerificationResetPasswordToken.objects.get(key=token_key)
    except VerificationResetPasswordToken.DoesNotExist:
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
        # A scenario where a user with a deleted account (when is_active set to false)
        # attempts to access this endpoint.
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

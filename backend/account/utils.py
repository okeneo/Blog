from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from .models import VerificationToken

User = get_user_model()

verification_url = "http://localhost:8000/blog/verify-email/?token_key={token_key}"
EMAIL_TEMPLATES = {
    "registration": {
        "subject": "Verify your email address",
        "message": verification_url,
    },
    "password_reset": {
        "subject": "Reset Password",
        "message": verification_url
        + "\nIf you didn't change it, you should click this link to recover it.",
    },
}


def send_verification_email(name, email, token_key, token=None):
    template = EMAIL_TEMPLATES.get(name)

    if template:
        subject = template["subject"]
        message = template["message"].format(token_key=token_key)
        send_mail(
            subject=subject,
            message=message,
            from_email=None,
            recipient_list=[email],
            fail_silently=True,
        )
    else:
        raise ValueError(f"Unsupported email template: {name}.")

    # Update the number of times we have attemped to send the user a verification email.
    if token:
        token.send_attempts += 1
        token.save(update_fields=["send_attempts"])


def perform_resend_verification(email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise ValidationError("User not found.")

    if user.is_active:
        raise ValidationError("User already registered.")

    try:
        token = VerificationToken.objects.get(user=user)
    except VerificationToken.DoesNotExist:
        # A scenario where a user with a deleted account (when is_active set to false)
        # attempts to access this endpoint.
        raise ValidationError("Unauthorized access.")

    if token.has_exceeded_maximum_attempts:
        raise ValidationError("Exceeded maximum send attempts.")

    return token, user

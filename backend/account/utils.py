from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.urls import reverse

from .models import VerificationToken

User = get_user_model()

# verification_url = reverse("email_confimation")
EMAIL_TEMPLATES = {
    "registration": {
        "subject": "Verify your email address",
        "message": "http://localhost:8000/blog/verify-email/?token_key={token_key}",
    },
    "forgot_password": {
        "subject": "Reset Password",
        "message": "http://localhost:8000/blog/verify-email/?token_key={token_key}"
        + "\nIf you didn't change it, you should.....?",
    },
    "update_email": {
        "subject": "Email Update Verification",
        "message": ""
        + "\nIf you didn't change it, you should click this link to recover it.",
    },
}


def send_verification_email(name, email, token_key):
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

from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_verification_email_task(template, email, token_key):
    from .controller import EMAIL_TEMPLATES

    template = EMAIL_TEMPLATES.get(template)
    if template:
        subject = template["subject"]
        message = template["message"].format(token_key=token_key)
        send_mail(
            subject=subject,
            message=message,
            from_email=None,
            recipient_list=[email],
            fail_silently=False,
        )
    else:
        raise ValueError(f"Unsupported email template: {template}.")

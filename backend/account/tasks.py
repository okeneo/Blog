from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_verification_email_task(subject, message, email):
    send_mail(
        subject=subject,
        message=message,
        from_email=None,
        recipient_list=[email],
        fail_silently=False,
    )

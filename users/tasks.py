from django.core.mail import send_mail

from celery import shared_task


@shared_task
def send_password_reset_email(email, reset_url):

    send_mail(
        subject="Password reset",
        message=f"""

Please go to the following link to reset your password:

{reset_url}

If it wasn't you, you can ignore this email.
""",
        from_email=None,
        recipient_list=[email],
    )

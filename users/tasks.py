from django.core.mail import send_mail

from celery import shared_task


@shared_task
def send_password_reset_email(email, reset_url):

    send_mail(
        subject="Восстановление пароля",
        message=f"""
Здравствуйте.

Для восстановления пароля перейдите по ссылке:

{reset_url}

Если это были не Вы — проигнорируйте письмо.
""",
        from_email=None,
        recipient_list=[email],
    )

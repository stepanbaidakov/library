from django.core.mail import send_mail
from django.utils import timezone

from celery import shared_task
from celery.utils.log import get_task_logger

from config.settings import DEFAULT_FROM_EMAIL
from library.models import Borrow

logger = get_task_logger("custom_logger")


@shared_task
def send_remind_email():
    borrows = Borrow.objects.filter(returned=False, due_date__lt=timezone.localdate())
    for borrow in borrows:
        try:
            send_mail(
                subject="Overdue book return",
                message=f"The rental period for the book {borrow.book.title} - {borrow.book.author} is overdue."
                f"Please return it as soon as possible.",
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=[borrow.user.email],
            )

        except Exception as e:
            logger.error(e)

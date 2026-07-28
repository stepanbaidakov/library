from django.utils import timezone

from rest_framework.serializers import ValidationError


class BorrowAvailableValidator:
    def __call__(self, attrs):
        book = attrs.get("book")
        if book and not book.is_available:
            raise ValidationError({"book": "Нет свободных книг для аренды"})


class DueDateValidator:
    def __call__(self, attrs):
        due_date = attrs.get("due_date")
        if due_date and due_date < timezone.localdate():
            raise ValidationError({"due_date": "Нельзя арендовать книгу на прошедшее время"})

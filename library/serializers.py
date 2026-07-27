from django.utils import timezone

from rest_framework import serializers

from .models import Author, Book, Borrow
from .validators import BorrowAvailableValidator, DueDateValidator


class BookSerializer(serializers.ModelSerializer):
    available_amount = serializers.ReadOnlyField()
    extra_kwargs = {
        "amount": {"write_only": True},
    }

    class Meta:
        model = Book
        fields = "__all__"
        read_only_fields = ("id",)
        ordering = ("-id",)
        extra_kwargs = {
            "amount": {"write_only": True},
        }

    def validate_year(self, value):
        if value > timezone.now().year:
            raise serializers.ValidationError({"year": "Год издания не может быть в будущем"})
        return value

    def validate(self, attrs):
        title = attrs.get("title", self.instance.title if self.instance else None)
        author = attrs.get("author", self.instance.author if self.instance else None)
        publisher = attrs.get("publisher", self.instance.publisher if self.instance else None)
        qs = Book.objects.filter(title=title, author=author, publisher=publisher)

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("У данного издания уже существует данная книга")
        return attrs


class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    books_count = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = "__all__"
        read_only_fields = ("id",)

    def get_books_count(self, obj):
        return Book.objects.filter(author=obj).count()

    def validate_birth_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError({"birth_date": "Дата рождения автора не может быть в будущем"})
        return value

    def validate(self, attrs):
        first_name = attrs.get("first_name", self.instance.first_name if self.instance else None)
        last_name = attrs.get("last_name", self.instance.last_name if self.instance else None)
        qs = Author.objects.filter(first_name=first_name, last_name=last_name)

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Такой автор уже существует")
        return attrs


class BorrowSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField()

    class Meta:
        model = Borrow
        exclude = ("returned",)
        read_only_fields = ("id", "issue_date", "returned_date", "user")
        validators = [BorrowAvailableValidator(), DueDateValidator()]

    def validate(self, attrs):
        user = self.context["request"].user
        book = attrs.get("book", self.instance.book if self.instance else None)
        qs = Borrow.objects.filter(user=user, book=book)

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError({"book": "Данная книга уже арендована Вами"})
        return attrs

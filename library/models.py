from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    birth_date = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    biography = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name_plural = "Authors"
        verbose_name = "Author"
        db_table = "author"
        ordering = ["pk"]


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    publisher = models.CharField(max_length=200, null=True, blank=True)
    genre = models.CharField(max_length=200, null=True, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    isbn = models.CharField(max_length=200, null=True, blank=True)
    amount = models.PositiveIntegerField(default=1)

    @property
    def available_amount(self):
        borrowed = self.borrows.filter(returned=False).count()
        return self.amount - borrowed

    @property
    def is_available(self):
        return self.available_amount > 0

    def __str__(self):
        return f"{self.title} - {self.author}"

    class Meta:
        db_table = "book"
        verbose_name_plural = "Books"
        verbose_name = "Book"
        ordering = ["pk"]


class Borrow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="borrows")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrows")
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned = models.BooleanField(default=False)
    returned_date = models.DateField(null=True, blank=True)

    @property
    def status(self):
        if self.returned:
            return "Возвращена"

        if timezone.localdate() > self.due_date:
            return "Просрочена"

        return "Выдана"

    def return_book(self):
        if not self.returned:
            self.returned = True
            self.returned_date = timezone.localdate()
            self.save()

    class Meta:
        ordering = ["pk"]

from django.contrib import admin

from .models import Author, Book, Borrow

# Register your models here.


class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author")
    search_fields = ("title", "author")
    list_filter = ("author",)
    ordering = ("id",)


admin.site.register(Book, BookAdmin)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name")
    search_fields = ("first_name", "last_name")
    list_filter = ("first_name", "last_name")
    ordering = ("id",)


admin.site.register(Author, AuthorAdmin)


class BorrowAdmin(admin.ModelAdmin):
    list_display = ("id", "book", "user")
    search_fields = ("book", "user")
    list_filter = ("book", "user")
    ordering = ("id",)


admin.site.register(Borrow, BorrowAdmin)

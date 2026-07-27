from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "phone", "full_name")
    fieldsets = UserAdmin.fieldsets + (
        (
            "Дополнительная информация",
            {
                "fields": ("phone",),
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Дополнительная информация",
            {
                "fields": ("phone",),
            },
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
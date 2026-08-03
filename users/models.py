from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=11, unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ("pk",)

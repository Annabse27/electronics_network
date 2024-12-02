from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Администратор"),
        ("manager", "Менеджер"),
        ("employee", "Сотрудник"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="employee")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username

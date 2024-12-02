from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser


# Форма для создания пользователя
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "role",
        )


# Форма для изменения пользователя
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "role",
        )


# Админка для CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    # Поля, отображаемые в списке пользователей
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "role",
        "date_joined",
    )
    list_filter = ("is_staff", "is_active", "role", "date_joined")

    # Поля, отображаемые при просмотре/редактировании пользователя
    fieldsets = (
        (
            "Основная информация",
            {"fields": ("username", "password", "email", "first_name", "last_name")},
        ),
        ("Права доступа", {"fields": ("is_staff", "is_active", "role")}),
        ("Дополнительно", {"fields": ("last_login", "date_joined")}),
    )

    # Поля, отображаемые при добавлении нового пользователя
    add_fieldsets = (
        (
            "Добавление нового пользователя",
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "role",
                ),
            },
        ),
    )

    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-date_joined",)

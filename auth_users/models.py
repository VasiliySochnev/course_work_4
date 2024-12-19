from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    country = models.CharField(blank=True, max_length=50)
    token = models.CharField(unique=True)
    total_attempt = models.IntegerField(verbose_name="Всего попыток рассылки", default=0)
    successful_attempt = models.IntegerField(verbose_name="Успешных попыток рассылки", default=0)
    unsuccessful_attempt = models.IntegerField(verbose_name="Неуспешных попыток рассылки", default=0)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        permissions = [("can_view_all_custom_user_lists", "can view all custom_user lists")]


class ResetPassword(models.Model):
    email = models.EmailField()

    class Meta:
        verbose_name = "сброс пароля"
        verbose_name_plural = "сброс паролей"
        db_table = "reset_password"

    def __str__(self):
        return self.email


class NewPassword(models.Model):
    email = models.EmailField()

    class Meta:
        verbose_name = "новый пароль"
        verbose_name_plural = "новый пароль"
        db_table = "new_password"

    def __str__(self):
        return self.email

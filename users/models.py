from django.contrib.auth.models import AbstractUser
from django.db import models

from catalog.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email", max_length=255)

    avatar = models.ImageField(upload_to='users/avatars', verbose_name="Аватар", **NULLABLE, help_text="Загрузите "
                                                                                                       "свой аватар")
    phone = models.CharField(max_length=35, verbose_name="Телефон", **NULLABLE, help_text="Введите номер телефона")
    country = models.CharField(max_length=255, verbose_name="Страна", help_text="Введите свою страну")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

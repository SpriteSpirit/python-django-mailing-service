from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    """ Пользователь """

    username = None

    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=100, verbose_name="Отчество", default="", **NULLABLE)
    phone_number = PhoneNumberField(verbose_name="Номер телефона", default="+7", **NULLABLE)
    avatar = models.ImageField(upload_to="users/avatars/", **NULLABLE)
    country = CountryField(blank_label="(select country)", verbose_name="Страна", default="RU")
    about_message = models.TextField(verbose_name="О себе", **NULLABLE)
    is_blocked = models.BooleanField(verbose_name="Заблокирован", default=False)

    # social messengers
    website = models.CharField(max_length=150, verbose_name="Сайт", default="https://", **NULLABLE)
    github = models.CharField(max_length=150, verbose_name="GitHub", default="", **NULLABLE)
    telegram = models.CharField(max_length=150, verbose_name="Telegram", default="@", **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

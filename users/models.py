from django.db import models
from django.contrib.auth.models import AbstractUser

from mailing_service.models import NULLABLE


class User(AbstractUser):
    """
    Пользователь
    """
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=100, verbose_name="Отчество", **NULLABLE)
    comment_about = models.TextField(verbose_name="Комментарий", **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

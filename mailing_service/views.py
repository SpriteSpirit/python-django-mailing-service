from django.db import models
from django.shortcuts import render

NULLABLE = {'null': True, 'blank': True}


def dashboard(request):
    return render(request, 'mailing_service/dashboard.html')


class Client(models.Model):
    name = models.CharField(max_length=150, verbose_name='Фамилия Имя Отчество')
    email = models.EmailField(verbose_name='Email')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Действующий')
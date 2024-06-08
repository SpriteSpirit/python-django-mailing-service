from django.db import models


NULLABLE = {'null': True, 'blank': True}


# Create your models here.
class Client(models.Model):
    """
    Клиент
    """
    objects = models.Manager()

    name = models.CharField(max_length=150, verbose_name='Фамилия Имя Отчество')
    email = models.EmailField(unique=True, verbose_name='Email')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Действующий')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} [{self.email}]'


class Message(models.Model):
    """ Сообщение для рассылки """

    objects = models.Manager()

    message_subject = models.CharField(max_length=150, verbose_name='Тема письма')
    message_body = models.TextField(verbose_name='Тело письма')
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ('message_subject',)

    def __str__(self):
        return f'{self.message_subject}'

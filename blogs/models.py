from django.db import models
from django.urls import reverse

from users.models import User


class BlogPost(models.Model):
    objects = models.Manager()

    title = models.CharField(max_length=250, verbose_name='Заголовок')
    slug = models.CharField(max_length=150, null=True, blank=True, verbose_name='slug')
    content = models.TextField(verbose_name='Содержание')
    image = models.ImageField(upload_to='blog_image/', blank=True, null=True, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    published = models.BooleanField(default=False, verbose_name='Опубликовано')
    view_count = models.PositiveIntegerField(default=0, verbose_name='Количеств просмотров')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('catalog:blogpost_detail', kwargs={'slug': self.slug})

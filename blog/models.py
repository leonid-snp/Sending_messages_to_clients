from django.db import models

from config.settings import NULLABLE


class Blog(models.Model):
    title = models.CharField(
        max_length=60,
        verbose_name='Заголовок',
        help_text='Напишите заголовок'
    )
    text = models.TextField(
        verbose_name='Текст статьи',
        help_text='Напишите текст статьи',
        **NULLABLE
    )
    image = models.ImageField(
        upload_to='blogs/',
        verbose_name='Изображение',
        help_text='Загрузите изображение',
        **NULLABLE
    )
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество просмотров',
        help_text='Укажите количество просмотров'
    )
    date = models.DateField(
        auto_now_add=True
    )
    date_update = models.DateField(
        auto_now=True
    )

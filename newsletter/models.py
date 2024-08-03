from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from config.settings import NULLABLE
from users.models import User


class Message(models.Model):
    subject = models.CharField(
        max_length=60,
        verbose_name='Тема',
        help_text='Напишите тему сообщения'
    )
    body = models.TextField(
        verbose_name='Сообщение',
        help_text='Напишите сообщение'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        help_text='Укажите автора',
        **NULLABLE
    )

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        permissions = [
            ('can_view_message', 'Can view message')
        ]


class Client(models.Model):
    email = models.EmailField(
        unique=True,
        max_length=60,
        verbose_name='Электронная почта',
        help_text='Укажите электронную почту'
    )
    phone = PhoneNumberField(
        unique=True,
        region='RU',
        verbose_name='Номер телефона',
        help_text='Введите номер телефона',
        **NULLABLE
    )
    full_name = models.CharField(
        unique=True,
        max_length=255,
        verbose_name='Ф.И.О.',
        help_text='Укажите Ф.И.О.',
        **NULLABLE
    )
    comment = models.CharField(
        max_length=60,
        verbose_name='Комментарий',
        help_text='Введите комментарий',
        **NULLABLE
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Укажите пользователя',
        **NULLABLE
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Newsletter(models.Model):
    MAILING_FREQUENCY_OPTIONS = {
        'OD': 'раз в день',
        'OW': 'раз в неделю',
        'OM': 'раз в месяц'
    }
    MAILING_STATUS_OPTIONS = {
        'CR': 'создана',
        'LA': 'запущена',
        'CO': 'завершена'
    }
    name = models.CharField(
        max_length=20,
        verbose_name='Название рассылки',
        help_text='Название рассылки',
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.SET_NULL,
        verbose_name='Сообщение',
        help_text='Выберите сообщение',
        **NULLABLE
    )
    clients = models.ManyToManyField(
        Client,
        verbose_name='Клиенты',
        help_text='Укажите клиентов',
        related_name='clients'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Укажите пользователя',
        **NULLABLE
    )
    date_time = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата и время',
        help_text='Укажите дату и время',
        **NULLABLE
    )
    periodicity = models.CharField(
        max_length=60,
        choices=MAILING_FREQUENCY_OPTIONS,
        verbose_name='Периодичность',
        help_text='Укажите периодичность',
        **NULLABLE
    )
    status = models.CharField(
        max_length=60,
        choices=MAILING_STATUS_OPTIONS,
        verbose_name='Статус рассылки',
        help_text='Укажите статус рассылки',
        default='CR'
    )

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class HistoryNewsletter(models.Model):
    date_time = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата и время',
        help_text='Укажите дату и время'
    )
    status = models.CharField(
        max_length=60,
        verbose_name='Статус рассылки',
        help_text='Укажите статус рассылки',
        **NULLABLE
    )
    response = models.CharField(
        max_length=60,
        verbose_name='Ответ почтового сервиса',
        help_text='Укажите ответ почтового сервиса',
        **NULLABLE
    )

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'

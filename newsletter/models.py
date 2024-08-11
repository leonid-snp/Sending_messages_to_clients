from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from config.settings import NULLABLE
from users.models import User


class Message(models.Model):
    """
    Модель сообщений.
    """
    subject = models.CharField(
        max_length=100,
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
            ('can_add_message', 'Can add message'),
            ('can_view_message', 'Can view message'),
            ('can_change_message', 'Can change message'),
            ('can_delete_message', 'Can delete message')
        ]


class Client(models.Model):
    """
    Модель клиентов.
    """
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
        max_length=100,
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
        permissions = [
            ('can_add_client', 'Can add client'),
            ('can_view_client', 'Can view client'),
            ('can_change_client', 'Can change client'),
            ('can_delete_client', 'Can delete client')
        ]


class Newsletter(models.Model):
    """
    Модель рассылки.
    """
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
        max_length=100,
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
        verbose_name='Дата и время создания',
        help_text='Укажите дату и время создания',
        **NULLABLE
    )
    date_start = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата начала рассылки',
        help_text='Укажите дату начала рассылки'
    )
    periodicity = models.CharField(
        max_length=100,
        choices=MAILING_FREQUENCY_OPTIONS,
        verbose_name='Периодичность',
        help_text='Укажите периодичность',
        **NULLABLE
    )
    status = models.CharField(
        max_length=100,
        choices=MAILING_STATUS_OPTIONS,
        verbose_name='Статус рассылки',
        help_text='Укажите статус рассылки',
        default='CR'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            ('can_add_newsletter', 'Can add newsletter'),
            ('can_view_newsletter', 'Can view newsletter'),
            ('can_change_newsletter', 'Can change newsletter'),
            ('can_delete_newsletter', 'Can delete newsletter')
        ]


class HistoryNewsletter(models.Model):
    """
    Модель попытки рассылки.
    """
    newsletter = models.ForeignKey(
        Newsletter,
        on_delete=models.SET_NULL,
        verbose_name='Рассылка',
        help_text='Укажите рассылку',
        **NULLABLE
    )
    date_time = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата и время рассылки',
        help_text='Укажите дату и время рассылки'
    )
    status = models.CharField(
        max_length=100,
        verbose_name='Статус рассылки',
        help_text='Укажите статус рассылки',
        **NULLABLE
    )
    response = models.CharField(
        max_length=255,
        verbose_name='Ответ почтового сервиса',
        help_text='Укажите ответ почтового сервиса',
        **NULLABLE
    )

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'

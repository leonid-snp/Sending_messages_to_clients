from django.contrib import admin
from django.contrib.admin import ModelAdmin

from newsletter.models import Client, HistoryNewsletter, Message, Newsletter


@admin.register(Message)
class MessageAdmin(ModelAdmin):
    """
    Регистрация модели сообщения в админке.
    """
    list_display = ('id', 'subject', 'body')
    search_fields = ('subject',)


@admin.register(Client)
class ClientAdmin(ModelAdmin):
    """
    Регистрация модели клиента в админке.
    """
    list_display = ('id', 'email', 'phone', 'comment')
    search_fields = ('email', 'phone')


@admin.register(Newsletter)
class NewsletterAdmin(ModelAdmin):
    """
    Регистрация модели рассылки в админке.
    """
    list_display = (
        'id', 'name', 'message', 'author', 'date_time', 'periodicity', 'status'
    )
    list_filter = (
        'message', 'clients', 'author', 'date_time', 'periodicity', 'status'
    )
    search_fields = ('id',)


@admin.register(HistoryNewsletter)
class HistoryNewsletterAdmin(ModelAdmin):
    """
    Регистрация модели попытки рассылки в админке.
    """
    list_display = ('id', 'newsletter', 'date_time', 'status', 'response')
    list_filter = ('status', 'response')

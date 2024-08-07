import smtplib
from datetime import datetime, timedelta

from django.core.cache import cache
from django.core.mail import send_mail

from blog.models import Blog
from config.settings import CACHE_ENABLED, EMAIL_HOST_USER
from newsletter.models import HistoryNewsletter, Newsletter


def __send_message(newsletter: iter) -> None:
    """
    Функция получает рассылку и создает функцию отправки
    затем сохраняет результат в историю независимо от результата.

    Parametrs:
    newsletter: (iter) - объект рассылки
    """
    try:
        server_response = send_mail(
            subject=newsletter.name,
            message=newsletter.message.body,
            from_email=EMAIL_HOST_USER,
            recipient_list=[client.email for client in newsletter._prefetched_objects_cache.get('clients')],
            fail_silently=False
        )
        HistoryNewsletter.objects.create(
            newsletter=newsletter,
            status='Отправлена',
            response=server_response
        )
    except smtplib.SMTPException as e:
        print(str(e))
        HistoryNewsletter.objects.create(
            newsletter=newsletter,
            status='Не отправлена',
            response=e
        )


def __check_mailing_date(newsletter: iter, days: int) -> None:
    """
    Функция получает рассылку и количество дней
    сравнивает дату старта отправки с сегодняшней
    если статус рассылки `создана` присваивает
    статус `запущена` и прибавляет количество дней
    для запуска в следующий раз после чего передает на отправку.

    Parametrs:
    newsletter: (iter) - объект рассылки
    days: (int) - количество дней
    """
    total_data = datetime.now().strftime('%Y-%m-%d %H:%M')
    total_data_start = newsletter.date_start.strftime('%Y-%m-%d %H:%M')
    if total_data_start == total_data:
        newsletter.status = 'LA'
        newsletter.date_start += timedelta(days=days)
        newsletter.save()
        __send_message(newsletter)


def get_newsletter() -> None:
    """
    Функция выбирает рассылки со статусом `создана` и `запущена`
    проверяет периодичность и отправляет рассылку
    в обработку в соответствии со значениями.
    """
    newsletter = (Newsletter.objects
                  .filter(status__in=['CR', 'LA'])
                  .prefetch_related('clients'))
    for item in newsletter:
        if item.periodicity == 'OD':
            __check_mailing_date(item, 1)
        elif item.periodicity == 'OW':
            __check_mailing_date(item, 7)
        else:
            __check_mailing_date(item, 31)


def get_blogs_from_cache():
    """
    Функция для получения статей бога из кеша,
    в случае если кеш пуст получает данные из бд.
    """
    if not CACHE_ENABLED:
        return Blog.objects.all()
    key = 'blogs_cache'
    blogs = cache.get(key)
    if blogs is not None:
        return blogs
    blogs = Blog.objects.all()
    cache.set(key, blogs)
    return blogs

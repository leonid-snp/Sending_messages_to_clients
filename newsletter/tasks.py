from celery import shared_task

from newsletter.services import get_newsletter


@shared_task()
def add_task():
    """
    Функция для запуска периодической задачи по расписанию.
    """
    get_newsletter()

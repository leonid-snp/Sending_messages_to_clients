from celery import shared_task

from newsletter.services import get_newsletter


@shared_task()
def test():
    """
    Функция для запуска периодической задачи по расписанию.
    """
    get_newsletter()

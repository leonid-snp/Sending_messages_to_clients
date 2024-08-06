from celery import shared_task
from newsletter.services import test_mailing


@shared_task()
def test():
    test_mailing()

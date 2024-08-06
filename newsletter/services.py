from datetime import datetime, timedelta

from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from newsletter.models import Newsletter


def mailing(newsletter):
    print(newsletter.name)
    print(newsletter.message.body)
    print(EMAIL_HOST_USER)
    print([client.email for client in newsletter._prefetched_objects_cache.get('clients')])
    send_mail(
        subject=newsletter.name,
        message=newsletter.message.body,
        from_email=EMAIL_HOST_USER,
        recipient_list=['leonidpetrov637@gmail.com', 'aigulamineva98@gmail.com']
    )


def __mailing(newsletter, days):
    total_data = datetime.now().strftime('%Y-%m-%d %H:%M')
    total_data_start = newsletter.date_start.strftime('%Y-%m-%d %H:%M')
    print(newsletter.date_start)
    if total_data_start == total_data:
        newsletter.status = 'LA'
        newsletter.date_start += timedelta(days=days)
        newsletter.save()
        mailing(newsletter)


def test_mailing():
    newsletter = (Newsletter.objects
                  .filter(status__in=['CR', 'LA'])
                  .prefetch_related('clients'))
    for item in newsletter:
        if item.periodicity == 'OD':
            __mailing(item, 1)
        elif item.periodicity == 'OW':
            __mailing(item, 7)
        else:
            __mailing(item, 31)

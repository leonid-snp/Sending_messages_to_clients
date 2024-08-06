import smtplib
from datetime import datetime, timedelta

from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from newsletter.models import Newsletter, HistoryNewsletter


def mailing(newsletter):
    try:
        server_response = send_mail(
            subject=newsletter.name,
            message=newsletter.message.body,
            from_email=EMAIL_HOST_USER,
            recipient_list=[client.email for client in newsletter._prefetched_objects_cache.get('clients')],
            fail_silently=False
        )
        # HistoryNewsletter.objects.create(
        #     newsletter=newsletter,
        #     status='Отправлена',
        #     response=server_response
        # )
    except smtplib.SMTPException as e:
        print(str(e))
        HistoryNewsletter.objects.create(
            newsletter=newsletter,
            status='Не отправлена',
            response=e
        )


def __mailing(newsletter, days):
    total_data = datetime.now().strftime('%Y-%m-%d %H:%M')
    total_data_start = newsletter.date_start.strftime('%Y-%m-%d %H:%M')
    mailing(newsletter)
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

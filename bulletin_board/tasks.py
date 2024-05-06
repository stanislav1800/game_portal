from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Bulletin, Category
import datetime
import time

@shared_task
def send_notifications(preview, pk, title, subscribers):
    print('send_notifications')
    html_content = render_to_string(
        'bulletin_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/board/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_week_notification():
    categories = Category.objects.all()
    for category in categories:
        subscribers = category.subscribers.all()
        bulletin = Bulletin.objects.filter(category=category, date__gte=datetime.datetime.now() - datetime.timedelta(days=7))
        if bulletin.exists():
            subject = f'Новые статьи в категории {category}'
            html_context = render_to_string(
                'weekly_notifications_email.html',
                {
                    'categ': category,
                    'bulletins': bulletin,
                    'link': f'{settings.SITE_URL}/news/'
                }
            )
            msg = EmailMultiAlternatives(
                subject=subject,
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[s.email for s in subscribers],
            )
            msg.attach_alternative(html_context, 'text/html')
            msg.send()


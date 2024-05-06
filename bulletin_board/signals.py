from django.db.models.signals import post_save
from .models import Response, BulletinToCategory, Category, Bulletin
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .tasks import send_notifications


def send_response_notification(response):
    bulletin_author = response.bulletin.author.user
    response_author = response.author.user
    subject = f'Новый отклик на ваше объявление "{strip_tags(response.bulletin.text)}"'
    message = f'Пользователь {response_author.username} откликнулся на ваше объявление "{strip_tags(response.bulletin.text)}".'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [bulletin_author.email]
    send_mail(subject, message, from_email, recipient_list)

def send_accepted_notification(response):
    response_author = response.author.user
    bulletin_author = response.bulletin.author.user
    subject = f'Ваш отклик на объявление "{strip_tags(response.bulletin.text)}" был принят'
    message = f'Пользователь {bulletin_author.username} принял ваш отклик на объявление "{strip_tags(response.bulletin.text)}".'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [response_author.email]
    send_mail(subject, message, from_email, recipient_list)

@receiver(post_save, sender=Response)
def send_response_notification_signal(sender, instance, created, **kwargs):
    if created:
        send_response_notification(instance)

@receiver(post_save, sender=Response)
def send_accepted_notification_signal(sender, instance, **kwargs):
    if instance.accepted:
        send_accepted_notification(instance)



@receiver(post_save, sender=Bulletin)
def notify_sub(sender, instance, created, **kwargs):
    if created:
        print('notify_sub')
        categories = instance.category.all()
        subscribers_emails = []
        for category in categories:
            subscribers = category.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]
        send_notifications.delay(instance.preview, instance.pk, instance.header, subscribers_emails)
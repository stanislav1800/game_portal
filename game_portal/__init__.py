from .celery import app as celery_app
# from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

__all__ = ('celery_app',)

# Устанавливаем настройки Django для Celery
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'game_portal.settings')
#
# app = Celery('game_portal')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()
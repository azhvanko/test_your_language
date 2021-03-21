import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_your_language.settings')

app = Celery('test_your_language')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

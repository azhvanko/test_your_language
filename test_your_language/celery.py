import os

from celery import Celery

from test_your_language.settings import ACTIVATION_LINK_LIFETIME


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_your_language.settings')

app = Celery('test_your_language')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'delete-deactivated-accounts': {
        'task': 'accounts.tasks.delete_deactivated_accounts',
        'schedule': ACTIVATION_LINK_LIFETIME // 2,
    }
}

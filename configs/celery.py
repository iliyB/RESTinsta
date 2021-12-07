
import os
from celery import Celery, platforms
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings')
platforms.C_FORCE_ROOT = True

app = Celery(
    'configs', backemd='amqp', broker=settings.CELERY_BROKER_URL,
    include=['instagram.tasks.periodic_tasks']
)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'update_data_about_users': {
        'task': 'instagram.tasks.periodic_tasks.update_data_about_users',
        'schedule': crontab(minute=0)
    },
}
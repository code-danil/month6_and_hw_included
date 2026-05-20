import os

from celery import Celery
from celery.beat import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_api.settings')

app = Celery('shop_api Celery')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-report_mail': {
        'task': 'users.tasks.send_report_mail',
        'schedule': crontab(month_of_year='1', day_of_month='1', minute='1'),
    },
}

app.conf.beat_schedule = {
    'send-report_mail': {
        'task': 'users.tasks.send_report_mail',
        'schedule': crontab(month_of_year='1', day_of_month='1', minute='1'),
    },
    'send-daily-stats': {
        'task': 'users.tasks.send_daily_stats',
        'schedule': crontab(hour='18', minute='1'),
    }
}
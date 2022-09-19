import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Celery beat tasks

app.conf.beat_schedule = {
    'send_ads_for_emails': {
        'task': 'user.tasks.send_ads_for_emails',
        'schedule': crontab(0, 0)
    },
    # 'parse_house_kg': {
    #     'task': 'advertisement.parser.tasks.parse_house_kg',
    #     'schedule': crontab(hour='*/1'),
    #     'args': (1, 5)
    # }
}

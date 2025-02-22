import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_profesor.settings')

app = Celery('app_profesor')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
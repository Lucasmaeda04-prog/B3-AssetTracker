import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'b3monitor.settings')

app = Celery('b3monitor')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-prices-every-minute': {
        'task': 'assets.tasks.programa_busca_ativo',
        'schedule': 60.0,  
    },
} 
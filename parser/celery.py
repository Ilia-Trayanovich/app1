from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Установите настройки Django по умолчанию для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('parser')

# Используйте настройки Django для конфигурации Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач в ваших приложениях
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')











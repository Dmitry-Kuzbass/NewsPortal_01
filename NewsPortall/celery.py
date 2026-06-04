# NewsPortal/celery.py
import os
from celery import Celery

# 1. Указываем Django, какой файл настроек использовать для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortall.settings')

# 2. Создаем экземпляр приложения Celery (в кавычках пишем имя папки проекта)
app = Celery('NewsPortall')

# 3. Говорим Celery читать все настройки, связанные с фоновыми задачами, прямо из settings.py.
# Названия настроек Celery в settings.py должны начинаться с префикса CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# 4. Автоматически ищем файлы tasks.py во всех зарегистрированных приложениях (например, в news/)
app.autodiscover_tasks()

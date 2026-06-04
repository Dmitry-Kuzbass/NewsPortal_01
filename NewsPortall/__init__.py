# NewsPortal/__init__.py
from .celery import app as celery_app

# Это гарантирует, что приложение Celery будет загружаться
# при каждом запуске Django.
__all__ = ('celery_app',)

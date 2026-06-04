# news/apps.py
from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        # ОСТАВЛЯЕМ ТОЛЬКО ЭТУ СТРОКУ:
        import news.signals

        # ВСЁ ОСТАЛЬНОЕ (scheduler.start(), scheduler.add_job и т.д.) УДАЛЯЕМ ОТСЮДА!
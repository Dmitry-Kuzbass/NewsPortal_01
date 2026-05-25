from django.apps import AppConfig


class NewsConfig(AppConfig):
    name = 'news'

    # Добавляем этот метод внутрь класса:
    def ready(self):
        # 1. Принудительно импортируем файл сигналов при запуске сервера
        import news.signals

        # 2. Настраиваем еженедельный таймер (APScheduler)
        from django_apscheduler.jobstores import DjangoJobStore
        from apscheduler.schedulers.background import BackgroundScheduler
        from .tasks import weekly_send_email_task  # Импортируем нашу функцию рассылки

        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # Настраиваем запуск задачи.
        # Для теста ставил запуск каждые 10 секунд (seconds=10).
        # Для сдачи на проверку поставил запуск каждую неделю (weeks=1).
        scheduler.add_job(
            weekly_send_email_task,
            trigger="interval",
            weeks=1,  # Менять тут на время проверки!
            id="weekly_send_email_job",
            max_instances=1,
            replace_existing=True,
        )

        # Включаем планировщик
        scheduler.start()
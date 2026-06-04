# news/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction  # ИСПРАВЛЕНО: Импортируем модуль транзакций
# Импортируем нашу новую фоновую задачу
from news.tasks import send_notifications_task


@receiver(post_save, sender='news.PostCategory')
def notify_subscribers(sender, instance, created, **kwargs):
    # Если в админке или на сайте успешно создалась связь новости с категорией
    if created:
        # Берем ID только что созданного поста
        post_id = instance.post.id

        # ВНИМАНИЕ: Вызываем задачу через .delay().
        # Это мгновенно бросает задачу в Redis и не тормозит работу сайта!
        #send_notifications_task.delay(post_id)

        # ИСПРАВЛЕНО: Говорим Django вызвать Celery только ПОСЛЕ того,
        # как база данных полностью запишет пост и разблокирует файл!
        transaction.on_commit(lambda: send_notifications_task.delay(post_id))

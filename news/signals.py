# news/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction  # ИСПРАВЛЕНО: Импортируем модуль транзакций
# Импортируем нашу новую фоновую задачу
from news.tasks import send_notifications_task
from django.core.cache import cache  # Импортируем модуль кэша

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


# СИГНАЛ СБРОСА КЭША: срабатывает при любом изменении модели Post
@receiver(post_save, sender='news.Post')
def clear_post_cache(sender, instance, **kwargs):
    # Формируем тот же уникальный ключ, по которому кэшировали статью
    cache_key = f'post-{instance.id}'
    # Принудительно удаляем старую копию из оперативной памяти Redis
    cache.delete(cache_key)
    print(f"--- Кэш для статьи post-{instance.id} успешно сброшен из-за изменений! ---")

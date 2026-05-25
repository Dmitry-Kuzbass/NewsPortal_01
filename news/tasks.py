# news/tasks.py
import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from news.models import Post, Category


def weekly_send_email_task():
    # 1. Вычисляем дату, которая была ровно 7 дней назад
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)

    # 2. Берем из базы данных все статьи, которые появились за эти 7 дней
    posts = Post.objects.filter(creation_time_date__gte=last_week)

    # Если за неделю не было ни одной новой статьи — останавливаем работу, слать нечего
    if not posts.exists():
        return

    # 3. Бежим по всем существующим категориям сайта
    categories = Category.objects.all()
    for category in categories:
        # Фильтруем статьи за неделю: оставляем только те, что относятся к текущей категории
        category_posts = posts.filter(category=category)

        # Если в этой категории появились статьи, и у неё есть подписчики
        if category_posts.exists() and category.subscribers.exists():
            # Собираем список email-адресов всех подписчиков этой категории
            subscribers_emails = [user.email for user in category.subscribers.all() if user.email]

            if subscribers_emails:
                subject = f"Еженедельный дайджест новых статей в разделе {category.name}"

                # Рендерим HTML-шаблон письма, передавая в него список статей и имя категории
                html_content = render_to_string(
                    'account/email/weekly_digest.html',
                    {
                        'link': 'http://127.0.0.1:8000',
                        'posts': category_posts,
                        'category_name': category.name,
                    }
                )

                # Текстовая заглушка
                text_content = f"Привет! Вот список новых статей за неделю в твоем любимом разделе {category.name}."

                # Отправляем одно общее письмо сразу всему списку подписчиков (to=[])
                # и скрываем их адреса друг от друга через bcc (скрытая копия)
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=None,
                    bcc=subscribers_emails  # Скрытая копия для безопасности адресов
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()

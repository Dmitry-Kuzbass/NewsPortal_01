# news/tasks.py
import datetime
from celery import shared_task  # Обязательный импорт для Celery
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from news.models import Post, Category


# --- ЗАДАЧА 1: Моментальное уведомление о новом посте через Celery ---
@shared_task
def send_notifications_task(post_id):
    try:
        # Находим созданный пост по его ID
        post = Post.objects.get(pk=post_id)

        # Ссылка на статью (используем имя вашей главной папки с одной 'l' - NewsPortal)
        full_url = f"http://127.0.0.1:8000{post.get_absolute_url()}"

        # Бежим по категориям и их подписчикам
        for category in post.category.all():
            for user in category.subscribers.all():
                if user.email:
                    subject = post.title

                    html_content = f"""
                    <h3>{post.title}</h3>
                    <p>{post.text[:50]}...</p>
                    <p>Здравствуй, {user.username}. Новая статья в твоём любимом разделе!</p>
                    <br>
                    <p><a href="{full_url}">Перейти и прочитать статью полностью</a></p>
                    """

                    text_content = f"{post.title}\n{post.text[:50]}...\nЗдравствуй, {user.username}.\nЧитать: {full_url}"

                    msg = EmailMultiAlternatives(
                        subject=subject,
                        body=text_content,
                        from_email=None,
                        to=[user.email]
                    )
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()

    except Post.DoesNotExist:
        pass


# --- ЗАДАЧА 2: Еженедельная рассылка дайджеста новостей ---
@shared_task
def weekly_send_email_task():
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(creation_time_date__gte=last_week)

    if not posts.exists():
        return

    categories = Category.objects.all()
    for category in categories:
        category_posts = posts.filter(category=category)

        if category_posts.exists() and category.subscribers.exists():
            subscribers_emails = [user.email for user in category.subscribers.all() if user.email]

            if subscribers_emails:
                subject = f"Еженедельный дайджест новых статей в разделе {category.name}"

                html_content = render_to_string(
                    'account/email/weekly_digest.html',
                    {
                        'link': 'http://127.0.0.1:8000',
                        'posts': category_posts,
                        'category_name': category.name,
                    }
                )

                text_content = f"Привет! Вот список новых статей за неделю в твоем разделе {category.name}."

                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=None,
                    bcc=subscribers_emails
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()

# news/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives


@receiver(post_save, sender='news.PostCategory')
def notify_subscribers(sender, instance, created, **kwargs):

    if created:

        try:
            from news.models import PostCategory, Category, Post

            category = instance.category
            post = instance.post

            # ШАГ 1: Собираем полную гиперссылку на статью
            # post.get_absolute_url() вернет строку вида '/news/ID/'
            # соединяем её с адресом локального сервера
            full_url = f"http://127.0.0.1:8000{post.get_absolute_url()}"


            for user in category.subscribers.all():

                if user.email:
                    subject = post.title

                    # ШАГ 2: Внедряем гиперссылку в HTML-код письма
                    html_content = f"""
                    <h3>{post.title}</h3>
                    <p>{post.text[:50]}...</p>
                    <p>Здравствуй, {user.username}. Новая статья в твоём любимом разделе!</p>
                    <br>
                    <p><a href="{full_url}" style="background-color: #007bff; color: white; padding: 8px 15px; text-decoration: none; border-radius: 4px; display: inline-block;">
                        Перейти и прочитать статью полностью
                    </a></p>
                    """

                    # Для текстовой версии (без HTML) просто даем ссылку чистым текстом
                    text_content = f"{post.title}\n{post.text[:50]}...\nЗдравствуй, {user.username}.\nПерейти к статье: {full_url}"


                    msg = EmailMultiAlternatives(
                        subject=subject,
                        body=text_content,
                        from_email=None,
                        to=[user.email]
                    )
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()


        except Exception as e:
            print(f"❌ КРИТИЧЕСКАЯ ОШИБКА ВНУТРИ СИГНАЛА: {e}")

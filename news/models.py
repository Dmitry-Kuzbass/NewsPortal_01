from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone
from django.urls import reverse #
from django.core.mail import EmailMultiAlternatives # Импортируем инструмент для HTML-писем

from allauth.account.signals import user_signed_up


# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = 0
        for post in self.post_set.all():
            post_rating += post.rating #суммарный рейтинг статьи автора

        comment_rating = 0
        for comment in self.user.comment_set.all():
            comment_rating += comment.rating #суммарный рейтинг всех комментариев автора

        post_comment_rating = 0
        for post in self.post_set.all():
            for comment in post.comment_set.all():
                post_comment_rating += comment.rating #суммарный рейтинг чужих комментариев к статьям автора

        self.rating = (post_rating * 3 ) + comment_rating + post_comment_rating #суммарный рейтинг всех комментариев к статьям автора
        self.save() #записываем полученный результат в таблицу

        # (Магический метод для красивого отображения автора):
    def __str__(self):
        # Возвращаем username связанного пользователя Django
        return self.user.username

class Category(models.Model): #модель категории
    name = models.CharField(unique=True)

    # Добавляем поле для подписчиков
    subscribers = models.ManyToManyField(User, related_name='categories', blank=True)

    def __str__(self):  # Для отображения объекта модели в виде текста, без него будет отображаться Category object (1)...
        return self.name

class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'

    POST_TYPE = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # связь оин ко многим к модели Author
    category = models.ManyToManyField(Category, through='PostCategory')  # связь многие ко многим через модель PostCategory

    post_type = models.CharField(max_length=2, choices=POST_TYPE, default=ARTICLE)
    creation_time_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, verbose_name='Заголовок статьи/новости') #заголовок статьи, второй аргумент позволяет выводить вместо title Заголовок
    text = models.TextField(verbose_name='Текст статьи/новости')  #текст статьи
    rating = models.IntegerField(default=0) #рейтинг статьи

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)]) #Чтобы после создания новости Django знал, куда перенаправить возвращает путь к новости



class PostCategory(models.Model): #промежуточная модель для связи многте ко многим
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    posts = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст комментария')  #текст комментария
    creation_time_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)  # рейтинг комментария

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()






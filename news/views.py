from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


# Create your views here.

# Представление для списка всех новостей
class NewsList(ListView):
    model = Post
    ordering = '-creation_time_date' # Сначала новые
    template_name = 'news.html'
    context_object_name = 'news'

# Представление для отдельной новости
class NewsDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
from django.shortcuts import render
from django.urls import reverse_lazy # Импорт для перенаправления после действий
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm # импорт формы!

# Create your views here.

# Представление для списка всех новостей
class NewsList(ListView):
    model = Post
    ordering = '-creation_time_date' # Сначала новые
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10 #строка включающая пагинацию, т.к. класс сам умеет делать пагинацию

# Представление для отдельной новости
class NewsDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    ordering = '-creation_time_date'
    template_name = 'search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш фильтр, передавая параметры из GET-запроса
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем отфильтрованный список
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем фильтр в контекст, чтобы вывести форму в шаблоне
        context['filterset'] = self.filterset
        return context

# Представления для НОВОСТЕЙ (News)
class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'NW' # Автоматически ставим тип "Новость"
        return super().form_valid(form)

class NewsUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


# Представления для СТАТЕЙ (Articles)
class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'AR' # Автоматически ставим тип "Статья"
        return super().form_valid(form)

class ArticleUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class ArticleDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')
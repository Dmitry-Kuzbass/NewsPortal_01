from django.shortcuts import render
from django.urls import reverse_lazy # Импорт для перенаправления после действий
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import Post
from .filters import PostFilter
from .forms import PostForm # импорт формы!
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin #импорт миксина для проверки авторизации пользователя

from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
# Create your views here.

# Представление для списка всех новостей
class NewsList(ListView):
    model = Post
    ordering = '-creation_time_date' # Сначала новые
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10 #строка включающая пагинацию, т.к. класс сам умеет делать пагинацию

    # Добавил метод, чтоб исчезала кнопка стать автором после нажатии данной кнопки
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем новую переменную в контекст
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context

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

# --- НОВЫЕ КЛАССЫ ДЛЯ CRUD ---

# Представления для НОВОСТЕЙ (News)
class NewsCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',) #провека права на создание
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'NW' # Автоматически ставим тип "Новость"
        return super().form_valid(form)

class NewsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class NewsDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


# Представления для СТАТЕЙ (Articles)
class ArticleCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)  # Право на создание объектов Post
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'AR' # Автоматически ставим тип "Статья"
        return super().form_valid(form)

class ArticleUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class ArticleDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')

@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('news_list') # После нажатия вернем пользователя на главную
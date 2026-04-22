from django_filters import FilterSet, DateTimeFilter, CharFilter
from django.forms import DateTimeInput
from .models import Post


class PostFilter(FilterSet):
    # Поиск по названию (регистронезависимый поиск подстроки)
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Название'
    )

    # Поиск по автору (через связанную модель)
    author = CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label='Автор'
    )

    # Позже указываемой даты
    added_after = DateTimeFilter(
        field_name='creation_time_date',
        lookup_expr='gt',
        label='Дата (позже)',
        widget=DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}),
    )

    class Meta:
        model = Post
        fields = ['title', 'author', 'added_after']
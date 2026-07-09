from django.contrib import admin
from .models import Post, Category, Author, PostCategory, Comment


# 1. Ваша встроенная форма для связи Пост-Категория
class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1  # Сколько пустых строк для выбора категорий показывать сразу


# 2. Настраиваем отображение самого Поста (объединяем колонки, фильтры и вашу inline-форму)
class PostAdmin(admin.ModelAdmin):
    # Добавляем удобные колонки в таблицу
    list_display = ('title', 'post_type', 'author', 'dateCreation', 'rating')

    # Добавляем фильтры справа
    list_filter = ('post_type', 'author', 'dateCreation')

    # Добавляем строку поиска сверху
    search_fields = ('title', 'text')

    # Подключаем вашу форму категорий внутрь страницы редактирования поста
    inlines = [PostCategoryInline]


# 3. Настройка для Комментариев
class CommentAdmin(admin.ModelAdmin):
    list_display = ('posts', 'author', 'creation_time_date', 'rating')
    list_filter = ('creation_time_date', 'rating')
    search_fields = ('text',)


# 4. Настройка для Авторов
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')
    search_fields = ('user__username',)


# 5. Регистрируем все модели в админке Django
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

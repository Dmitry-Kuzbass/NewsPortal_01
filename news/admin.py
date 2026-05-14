from django.contrib import admin
from .models import Post, Category, Author, PostCategory  # импортируйте ваши модели


# Register your models here.

# 1. Создаем встроенную форму для связи Пост-Категория
class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1  # Сколько пустых строк для выбора категорий показывать сразу

# 2. Настраиваем отображение самого Поста
class PostAdmin(admin.ModelAdmin):
    inlines = [PostCategoryInline] # Подключаем наши категории внутрь поста

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Author)
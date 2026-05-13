from django.urls import path
from .views import(
    NewsList, NewsDetail, PostSearch,
    NewsCreate, NewsUpdate, NewsDelete,
    ArticleCreate, ArticleUpdate, ArticleDelete,
    upgrade_me
)

urlpatterns = [
    # Путь для списка новостей: /news/
    path('', NewsList.as_view(), name='news_list'),
    # Путь для одной новости: /news/<id>
    path('<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),


    # --- НОВОСТИ (NEWS) ---
    # Ссылка: /news/create/
    path('create/', NewsCreate.as_view(), name='news_create'),
    # Ссылка: /news/<id>/edit/
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    # Ссылка: /news/<id>/delete/
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),

    # --- СТАТЬИ (ARTICLES) ---
    # Ссылка: /news/articles/create/
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    # Ссылка: /news/articles/<id>/edit/
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
    # Ссылка: /news/articles/<int:pk>/delete/
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    #
    path('upgrade/', upgrade_me, name='upgrade'),

]


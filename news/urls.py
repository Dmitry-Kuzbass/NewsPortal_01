from django.urls import path
from .views import NewsList, NewsDetail

urlpatterns = [
    # Путь для списка новостей: /news/
    path('', NewsList.as_view(), name='news_list'),
    # Путь для одной новости: /news/<id>
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
]
from django.urls import path
from . import views
from .models import Post

urlpatterns = [
    path('news/', views.news_list, name='news_list'),
    path('news/<int:id>/', views.news_detail, name='news_detail'),
]

# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Новости
    path('news/create/', lambda request: views.create_post(request, Post.NEWS), name='create_news'),
    path('news/<int:pk>/edit/', lambda request, pk: views.edit_post(request, pk, Post.NEWS), name='edit_news'),
    path('news/<int:pk>/delete/', lambda request, pk: views.delete_post(request, pk, Post.NEWS), name='delete_news'),

    # Статьи
    path('articles/create/', lambda request: views.create_post(request, Post.ARTICLE), name='create_article'),
    path('articles/<int:pk>/edit/', lambda request, pk: views.edit_post(request, pk, Post.ARTICLE), name='edit_article'),
    path('articles/<int:pk>/delete/', lambda request, pk: views.delete_post(request, pk, Post.ARTICLE), name='delete_article'),
]

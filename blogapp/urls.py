# blogapp/urls.py
from django.urls import path
from . import views  # Импортируем представления из текущего приложения
from .views import (
    PostListAPIView, PostDetailAPIView, PostCreateAPIView, PostUpdateDestroyAPIView,
    CommentListAPIView, CommentCreateAPIView, CommentUpdateDestroyAPIView
)
urlpatterns = [
    path('inspiration/', views.inspiration, name='inspiration'),  # Страница "Блог"
    path('create/', views.create_post, name='create_post'),  # Создание поста
    path('post/<int:pk>/', views.post_detail, name='post_detail'),  # Детали поста
    path('edit_post/<int:pk>/', views.edit_post, name='edit_post'),  # Редактирование поста
    path('delete_post/<int:pk>/', views.delete_post, name='delete_post'),  # Удаление поста
# Маршруты для постов
    path('api/posts/', PostListAPIView.as_view(), name='post-list'),
    path('api/posts/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('api/posts/create/', PostCreateAPIView.as_view(), name='post-create'),
    path('api/posts/<int:pk>/edit/', PostUpdateDestroyAPIView.as_view(), name='post-update-destroy'),

    # Маршруты для комментариев
    path('api/comments/', CommentListAPIView.as_view(), name='comment-list'),
    path('api/comments/create/', CommentCreateAPIView.as_view(), name='comment-create'),
    path('api/comments/<int:pk>/edit/', CommentUpdateDestroyAPIView.as_view(), name='comment-update-destroy'),
]
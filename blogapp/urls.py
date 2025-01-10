# blogapp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    inspiration, create_post, post_detail, edit_post, delete_post,  # Ваши существующие представления
    PostViewSet, CommentViewSet, TagViewSet  # Новые ViewSet для API
)

# Создаем роутер и регистрируем ViewSet
router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    # Ваши существующие маршруты
    path('inspiration/', inspiration, name='inspiration'),  # Страница "Блог"
    path('create/', create_post, name='create_post'),  # Создание поста
    path('post/<int:pk>/', post_detail, name='post_detail'),  # Детали поста
    path('edit_post/<int:pk>/', edit_post, name='edit_post'),  # Редактирование поста
    path('delete_post/<int:pk>/', delete_post, name='delete_post'),  # Удаление поста

    # Добавляем маршруты API
    path('api/', include(router.urls)),  # Все API-маршруты будут начинаться с /blog/api/
]
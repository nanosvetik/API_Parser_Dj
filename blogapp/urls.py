from django.urls import path
from . import views  # Импортируем представления из текущего приложения

urlpatterns = [
    path('inspiration/', views.inspiration, name='inspiration'),  # Страница "Блог"
    path('create/', views.create_post, name='create_post'),  # Создание поста
    path('post/<int:pk>/', views.post_detail, name='post_detail'),  # Детали поста
    path('edit_post/<int:pk>/', views.edit_post, name='edit_post'),  # Редактирование поста
    path('delete_post/<int:pk>/', views.delete_post, name='delete_post'),  # Удаление поста
]
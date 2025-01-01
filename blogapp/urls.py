from django.urls import path
from . import views

urlpatterns = [
    path('inspiration/', views.inspiration, name='inspiration'),  # Страница "Блог"
    path('create/', views.create_post, name='create_post'),  # Создание поста
    path('post/<int:pk>/', views.post_detail, name='post_detail'),  # Детали поста

]
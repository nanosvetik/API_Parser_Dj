# userapp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    register, user_login, user_logout, profile, edit_user_role, user_list, request_author_status, notifications,  # Ваши существующие представления
    UserProfileViewSet, NotificationViewSet  # Новые ViewSet для API
)

# Создаем роутер и регистрируем ViewSet
router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    # Ваши существующие маршруты
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('edit_user_role/<int:user_id>/', edit_user_role, name='edit_user_role'),
    path('request_author_status/', request_author_status, name='request_author_status'),
    path('notifications/', notifications, name='notifications'),

    # Добавляем маршруты API
    path('api/', include(router.urls)),  # Все API-маршруты будут начинаться с /user/api/
]
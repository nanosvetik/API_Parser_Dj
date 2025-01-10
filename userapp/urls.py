from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token  # Встроенное представление для получения токена
from .views import (
    register, user_login, user_logout, profile, edit_user_role, user_list, request_author_status, notifications,
    UserProfileViewSet, NotificationViewSet, refresh_token, get_token  # Импортируем все представления
)

# Создаем роутер и регистрируем ViewSet
router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)  # Регистрируем ViewSet для профилей
router.register(r'notifications', NotificationViewSet)  # Регистрируем ViewSet для уведомлений

urlpatterns = [
    # Ваши существующие маршруты
    path('register/', register, name='register'),  # Регистрация
    path('login/', user_login, name='login'),  # Вход
    path('logout/', user_logout, name='logout'),  # Выход
    path('profile/', profile, name='profile'),  # Личный кабинет
    path('edit_user_role/<int:user_id>/', edit_user_role, name='edit_user_role'),  # Редактирование роли пользователя
    path('request_author_status/', request_author_status, name='request_author_status'),  # Запрос статуса "автор"
    path('notifications/', notifications, name='notifications'),  # Уведомления

    # Маршруты для работы с токенами
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # Получение токена (для внешних запросов)
    path('api-token-refresh/', refresh_token, name='api_token_refresh'),  # Обновление токена
    path('api-token-get/', get_token, name='api_token_get'),  # Получение токена для текущего пользователя

    # Маршруты API
    path('api/', include(router.urls)),  # Все API-маршруты будут начинаться с /user/api/
]
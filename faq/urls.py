# faq/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import faq, FAQViewSet  # Импортируем представления

# Создаем роутер и регистрируем ViewSet
router = DefaultRouter()
router.register(r'faqs', FAQViewSet)

urlpatterns = [
    # Ваш существующий маршрут
    path('faq/', faq, name='faq'),  # Маршрут для FAQ

    # Добавляем маршруты API
    path('api/', include(router.urls)),  # Все API-маршруты будут начинаться с /faq/api/
]
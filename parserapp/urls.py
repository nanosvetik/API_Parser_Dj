# parserapp/urls.py
from django.urls import path, include  # Добавляем импорт include
from rest_framework.routers import DefaultRouter
from .views import SkillViewSet, VacancyViewSet, IndexView, VacancySearchView, ResultsView, ContactView, StatisticsView

# Создаем роутер и регистрируем ViewSet
router = DefaultRouter()
router.register(r'skills', SkillViewSet)
router.register(r'vacancies', VacancyViewSet)

urlpatterns = [
    # Ваши существующие маршруты
    path('', IndexView.as_view(), name='index'),  # Главная страница
    path('form/', VacancySearchView.as_view(), name='form'),  # Форма поиска
    path('results/', ResultsView.as_view(), name='results'),  # Результаты
    path('statistics/', StatisticsView.as_view(), name='statistics'),  # Статистика
    path('contact/', ContactView.as_view(), name='contact'),  # Контакты

    # Добавляем маршруты API
    path('api/', include(router.urls)),  # Все API-маршруты будут начинаться с /api/
]
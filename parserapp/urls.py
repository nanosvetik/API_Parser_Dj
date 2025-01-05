# parserapp/urls.py
from django.urls import path
from .views import IndexView, VacancySearchView, ResultsView, ContactView, StatisticsView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),  # Главная страница
    path('form/', VacancySearchView.as_view(), name='form'),  # Форма поиска
    path('results/', ResultsView.as_view(), name='results'),  # Результаты
    path('statistics/', StatisticsView.as_view(), name='statistics'),  # Статистика
    path('contact/', ContactView.as_view(), name='contact'),  # Контакты
]
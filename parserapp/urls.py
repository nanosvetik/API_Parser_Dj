# parserapp/urls.py
from django.urls import path
from .views import IndexView, VacancySearchView, ResultsView, ContactView, StatisticsView
from .views import VacancyListAPIView, VacancyDetailAPIView, SkillListAPIView,  VacancySearchAPIView, HomePageAPIView, ContactPageAPIView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),  # Главная страница
    path('form/', VacancySearchView.as_view(), name='form'),  # Форма поиска
    path('results/', ResultsView.as_view(), name='results'),  # Результаты
    path('statistics/', StatisticsView.as_view(), name='statistics'),  # Статистика
    path('contact/', ContactView.as_view(), name='contact'),  # Контакты
    path('api/vacancies/', VacancyListAPIView.as_view(), name='vacancy-list'),
    path('api/vacancies/<int:pk>/', VacancyDetailAPIView.as_view(), name='vacancy-detail'),
    path('api/skills/', SkillListAPIView.as_view(), name='skill-list'),
    path('api/search/', VacancySearchAPIView.as_view(), name='vacancy-search'),
    path('api/home/', HomePageAPIView.as_view(), name='home-api'),
    path('api/contact/', ContactPageAPIView.as_view(), name='contact-api'),
]
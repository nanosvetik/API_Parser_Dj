# faq/urls.py
from django.urls import path
from . import views
from .views import FAQListAPIView, FAQCreateAPIView, FAQDetailAPIView

urlpatterns = [
    path('', views.faq, name='faq'),  # Маршрут для FAQ (теперь это корневой путь для faq/)
    path('api/faq/', FAQListAPIView.as_view(), name='faq-list'),  # API для списка FAQ
    path('api/faq/create/', FAQCreateAPIView.as_view(), name='faq-create'),  # API для создания FAQ
    path('api/faq/<int:pk>/', FAQDetailAPIView.as_view(), name='faq-detail'),  # API для редактирования/удаления FAQ
]
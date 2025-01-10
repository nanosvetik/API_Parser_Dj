# faq/views.py
from django.shortcuts import render
from .models import FAQ

# Импорты для Django REST Framework
from rest_framework import viewsets
from .serializers import FAQSerializer

def faq(request):
    """
    Представление для отображения FAQ, сгруппированного по категориям.
    """
    # Группируем вопросы по категориям
    faqs = FAQ.objects.all().order_by('category', 'created_at')
    faqs_by_category = {}
    for faq in faqs:
        if faq.category not in faqs_by_category:
            faqs_by_category[faq.category] = []
        faqs_by_category[faq.category].append(faq)

    return render(request, 'faq/faq.html', {'faqs_by_category': faqs_by_category})

# ViewSet для модели FAQ
class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
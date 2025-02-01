from django.shortcuts import render
from .models import FAQ

from rest_framework import generics, permissions
from .models import FAQ
from .serializers import FAQSerializer

def faq(request):
    # Группируем вопросы по категориям
    faqs = FAQ.objects.all().order_by('category', 'created_at')
    faqs_by_category = {}
    for faq in faqs:
        if faq.category not in faqs_by_category:
            faqs_by_category[faq.category] = []
        faqs_by_category[faq.category].append(faq)

    return render(request, 'faq/faq.html', {'faqs_by_category': faqs_by_category})

# Для чтения (доступно всем)
class FAQListAPIView(generics.ListAPIView):
    queryset = FAQ.objects.all().order_by('category', 'created_at')
    serializer_class = FAQSerializer
    permission_classes = [permissions.AllowAny]  # Доступ у всех

# Для создания (доступно только админам)
class FAQCreateAPIView(generics.CreateAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [permissions.IsAdminUser]  # Доступ только у админов

# Для редактирования и удаления (доступно только админам)
class FAQDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [permissions.IsAdminUser]  # Доступ только у админов

from django.shortcuts import render
from .models import FAQ


def faq(request):
    # Группируем вопросы по категориям
    faqs = FAQ.objects.all().order_by('category', 'created_at')
    faqs_by_category = {}
    for faq in faqs:
        if faq.category not in faqs_by_category:
            faqs_by_category[faq.category] = []
        faqs_by_category[faq.category].append(faq)

    return render(request, 'faq/faq.html', {'faqs_by_category': faqs_by_category})

# Create your views here.

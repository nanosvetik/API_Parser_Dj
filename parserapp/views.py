# parserapp/views.py
from django.views.generic import TemplateView, FormView, ListView
from django.db.models import Count
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from .forms import VacancySearchForm
from .models import Vacancy, Skill
from .services import get_area_id
from .management.commands.fill_database import Command as FillDatabaseCommand

from rest_framework import generics
from .models import Vacancy, Skill
from .serializers import VacancySerializer, SkillSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import VacancySearchSerializer
from .serializers import HomePageSerializer
from .serializers import ContactPageSerializer

# Главная страница
class IndexView(TemplateView):
    template_name = 'index.html'

# Форма поиска вакансий
class VacancySearchView(FormView):
    template_name = 'form.html'
    form_class = VacancySearchForm
    success_url = '/results/'

    def form_valid(self, form):
        job_title = form.cleaned_data['title']
        location_name = form.cleaned_data['location']
        experience = form.cleaned_data['experience']
        work_format = form.cleaned_data['work_format']  # Новое поле
        employment_type = form.cleaned_data['employment_type']  # Новое поле

        if not job_title:
            messages.error(self.request, 'Профессия не указана.')
            return super().form_valid(form)

        # Преобразуем название региона в ID
        location_id = None
        if location_name:
            location_id = get_area_id(location_name)
            if not location_id:
                messages.error(self.request, f'Регион "{location_name}" не найден.')
                return super().form_valid(form)

        # Сохраняем параметры поиска в сессии
        self.request.session['search_params'] = {
            'title': job_title,
            'location': location_name,
            'experience': experience,
            'work_format': work_format,  # Новое поле
            'employment_type': employment_type,  # Новое поле
        }

        # Запускаем парсер с указанными параметрами
        fill_database_command = FillDatabaseCommand()
        fill_database_command.handle(
            profession=job_title,
            experience=experience,
            work_format=work_format,  # Новое поле
            employment_type=employment_type,  # Новое поле
            location=location_id if location_id else 1  # Передаем 1 (Москва), если регион не указан
        )

        return super().form_valid(form)

# Страница с результатами поиска
class ResultsView(ListView):
    template_name = 'results.html'
    context_object_name = 'vacancies'
    paginate_by = 20

    def get_queryset(self):
        # Возвращаем все вакансии, отсортированные по id
        return Vacancy.objects.all().order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем топ-10 навыков по количеству связанных вакансий
        top_skills = Skill.objects.annotate(vacancy_count=Count('vacancies')).order_by('-vacancy_count')[:10]
        context['skills'] = top_skills  # Добавляем навыки в контекст шаблона

        return context

# Страница контактов
class ContactView(TemplateView):
    template_name = 'contact.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        if name and email and message:
            subject = f"Сообщение от {name} ({email})"
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            messages.success(request, 'Сообщение отправлено!')
        else:
            messages.error(request, 'Все поля обязательны для заполнения.')
        return redirect('contact')

# Страница статистики
class StatisticsView(TemplateView):
    template_name = 'statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем количество вакансий для каждого навыка
        skills_with_count = Skill.objects.annotate(vacancy_count=Count('vacancies')).order_by('-vacancy_count')
        context['skills_with_count'] = skills_with_count
        return context



class VacancyListAPIView(generics.ListAPIView):
    queryset = Vacancy.objects.all().order_by('-created_at')
    serializer_class = VacancySerializer

class VacancyDetailAPIView(generics.RetrieveAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer

class SkillListAPIView(generics.ListAPIView):
    queryset = Skill.objects.annotate(vacancy_count=Count('vacancies')).order_by('-vacancy_count')
    serializer_class = SkillSerializer


class VacancySearchAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Валидация входных данных
        serializer = VacancySearchSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Извлекаем параметры поиска
        profession = serializer.validated_data['profession']
        experience = serializer.validated_data.get('experience', 'noExperience')
        work_format = serializer.validated_data.get('work_format', None)
        employment_type = serializer.validated_data.get('employment_type', None)
        location = serializer.validated_data.get('location', 1)

        # Запускаем парсер
        fill_database_command = FillDatabaseCommand()
        try:
            fill_database_command.handle(
                profession=profession,
                experience=experience,
                work_format=work_format,
                employment_type=employment_type,
                location=location
            )
            return Response({"message": "Поиск вакансий успешно запущен"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class HomePageAPIView(APIView):
    def get(self, request, *args, **kwargs):
        data = {
            "title": "Добро пожаловать на Parser HH",
            "description": "Найди свою работу мечты с Parser HH, быстро и удобно!",
            "features": [
                {"title": "Быстрый результат", "description": "Получение списка вакансий одним нажатием кнопки."},
                {"title": "Список навыков", "description": "Узнай, какие навыки самые востребованные."},
                {"title": "Удобный поиск", "description": "Просто выбери необходимые параметры поиска."},
                {"title": "Блог", "description": "Полезные статьи и истории пользователей."},
            ]
        }
        serializer = HomePageSerializer(data)
        return Response(serializer.data)


class ContactPageAPIView(APIView):
    def get(self, request, *args, **kwargs):
        data = {
            "title": "Всегда рада обратной связи",
            "description": "Если у вас есть вопросы, предложения по улучшению и развитию проекта, свяжитесь со мной.",
            "contacts": [
                {
                    "type": "Telegram",
                    "value": "@Svetlana_F80",
                    "link": "https://t.me/Svetlana_F80"
                },
                {
                    "type": "Сообщество",
                    "value": "Истории пользователей",
                    "link": "{% url 'inspiration' %}"
                },
                {
                    "type": "FAQ",
                    "value": "Часто задаваемые вопросы",
                    "link": "{% url 'faq' %}"
                }
            ]
        }
        serializer = ContactPageSerializer(data)
        return Response(serializer.data)
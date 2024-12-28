from django.views.generic import TemplateView, FormView, ListView
from django.db.models import Count
from .forms import VacancySearchForm
from .management.commands.fill_database import Command as FillDatabaseCommand
from .models import Vacancy, Skill

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
        location = form.cleaned_data['location']
        experience = form.cleaned_data['experience']
        schedule = form.cleaned_data['schedule']

        # Сохраняем параметры поиска в сессии
        self.request.session['search_params'] = {
            'title': job_title,
            'location': location,
            'experience': experience,
            'schedule': schedule,
        }

        # Запускаем парсер с указанными параметрами
        fill_database_command = FillDatabaseCommand()
        fill_database_command.handle(
            search_text=job_title,
            experience=experience,
            schedule=schedule,
            location=location
        )

        return super().form_valid(form)


# Страница с результатами поиска
class ResultsView(ListView):
    template_name = 'results.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        # Возвращаем все вакансии
        return Vacancy.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем топ-10 навыков по количеству связанных вакансий
        top_skills = Skill.objects.annotate(vacancy_count=Count('vacancies')).order_by('-vacancy_count')[:10]
        context['skills'] = top_skills

        return context

# Страница контактов
class ContactView(TemplateView):
    template_name = 'contact.html'

# Страница статистики
class StatisticsView(TemplateView):
    template_name = 'statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем количество вакансий для каждого навыка
        skills_with_count = Skill.objects.annotate(vacancy_count=Count('vacancies'))
        context['skills_with_count'] = skills_with_count
        return context
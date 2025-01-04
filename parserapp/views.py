from django.views.generic import TemplateView, FormView, ListView
from django.db.models import Count
from .forms import VacancySearchForm
from .management.commands.fill_database import Command as FillDatabaseCommand
from .models import Vacancy, Skill
from .services import get_area_id

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
        location_name = form.cleaned_data['location']  # Название региона
        experience = form.cleaned_data['experience']
        schedule = form.cleaned_data['schedule']

        if not job_title:
            self.stdout.write(self.style.ERROR('Профессия не указана.'))
            return super().form_valid(form)

        # Преобразуем название региона в ID
        location_id = None
        if location_name:
            location_id = get_area_id(location_name)
            if not location_id:
                self.stdout.write(self.style.ERROR(f'Регион "{location_name}" не найден.'))
                return super().form_valid(form)

        # Сохраняем параметры поиска в сессии
        self.request.session['search_params'] = {
            'title': job_title,
            'location': location_name,
            'experience': experience,
            'schedule': schedule,
        }

        # Запускаем парсер с указанными параметрами
        fill_database_command = FillDatabaseCommand()
        fill_database_command.handle(
            profession=job_title,
            experience=experience,
            schedule=schedule,
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
        skills_with_count = Skill.objects.annotate(vacancy_count=Count('vacancies')).order_by('-vacancy_count')
        context['skills_with_count'] = skills_with_count
        return context
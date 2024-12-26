from django.shortcuts import render, redirect
from .forms import VacancySearchForm
from .management.commands.fill_database import Command as FillDatabaseCommand
from .models import Vacancy, Skill

def index(request):
    return render(request, 'index.html')
# Форма поиска
def form(request):
    if request.method == 'POST':
        form = VacancySearchForm(request.POST)
        if form.is_valid():
            # Получаем данные из формы
            job_title = form.cleaned_data['title']
            location = form.cleaned_data['location']
            experience = form.cleaned_data['experience']
            schedule = form.cleaned_data['schedule']

            # Запускаем парсер с указанными параметрами
            fill_database_command = FillDatabaseCommand()
            fill_database_command.handle(
                search_text=job_title,
                experience=experience,
                schedule=schedule,
                location=location
            )

            # Перенаправляем на страницу с результатами
            return redirect('results')  # Используем redirect
    else:
        form = VacancySearchForm()

    return render(request, 'form.html', {'form': form})

# Результаты поиска
def results(request):
    # Фильтруем вакансии и навыки по параметрам (если они есть)
    vacancies = Vacancy.objects.all()
    skills = Skill.objects.all()

    # Передаем данные в шаблон
    return render(request, 'results.html', {
        'vacancies': vacancies,
        'skills': skills,
    })
# Контакты
def contact(request):
    return render(request, 'contact.html')
# parserapp/forms.py
from django import forms
from .models import Vacancy

class VacancySearchForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ['title', 'location', 'experience', 'work_format', 'employment_type']  # Убрали schedule, добавили work_format и employment_type
        labels = {
            'title': 'Введите название вакансии',
            'location': 'Где искать (опционально)',
            'experience': 'Опыт работы',
            'work_format': 'Формат работы (опционально)',  # Новое поле
            'employment_type': 'Тип занятости (опционально)',  # Новое поле
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например, Python разработчик'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Город или страна'}),
            'experience': forms.Select(choices=[
                ('noExperience', 'Без опыта'),
                ('between1And3', 'От 1 до 3 лет'),
                ('between3And6', 'От 3 до 6 лет'),
                ('moreThan6', 'Более 6 лет'),
            ], attrs={'class': 'form-select'}),
            'work_format': forms.Select(choices=[
                ('', 'Не указано'),
                ('remote', 'Удаленно'),
                ('hybrid', 'Гибрид'),
                ('office', 'Офис'),
            ], attrs={'class': 'form-select'}),
            'employment_type': forms.Select(choices=[
                ('', 'Не указано'),
                ('fullDay', 'Полный день'),
                ('partTime', 'Частичная занятость'),
                ('flexible', 'Гибкий график'),
            ], attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].required = False
        self.fields['work_format'].required = False  # Делаем поле необязательным
        self.fields['employment_type'].required = False  # Делаем поле необязательным
from django import forms
from .models import Vacancy

class VacancySearchForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ['title', 'location', 'experience', 'schedule']
        labels = {
            'title': 'Введите название вакансии',
            'location': 'Где искать (опционально)',
            'experience': 'Опыт работы',
            'schedule': 'Тип занятости',
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
            'schedule': forms.Select(choices=[
                ('remote', 'Удаленная работа'),
                ('fullDay', 'Полный день'),
                ('partTime', 'Частичная занятость'),
                ('flexible', 'Гибкий график'),
            ], attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].required = False  # Делаем поле location необязательным
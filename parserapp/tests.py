from django.test import TestCase
from parserapp.models import Skill, Vacancy

class SkillModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестовые данные
        cls.skill = Skill.objects.create(name='Python')

    def test_skill_creation(self):
        self.assertEqual(self.skill.name, 'Python')
        self.assertEqual(str(self.skill), 'Python')  # Проверка метода __str__

class VacancyModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестовые данные
        cls.vacancy = Vacancy.objects.create(
            title='Python Developer',
            description='Описание вакансии',
            url='https://example.com',
            location='Москва',
            experience='noExperience',
            schedule='remote'
        )

    def test_vacancy_creation(self):
        self.assertEqual(self.vacancy.title, 'Python Developer')
        self.assertEqual(self.vacancy.location, 'Москва')

# Create your tests here.

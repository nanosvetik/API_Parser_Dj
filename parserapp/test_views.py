from django.test import TestCase, Client
from django.urls import reverse
from parserapp.forms import VacancySearchForm

class VacancySearchViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('form')  # Используем правильное имя маршрута

    def test_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], VacancySearchForm)

    def test_post_request(self):
        data = {
            'title': 'Python разработчик',
            'location': 'Москва',
            'experience': 'noExperience',
            'schedule': 'remote',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Проверка перенаправления
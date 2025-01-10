from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token


class TokenAuthenticationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url_get_token = reverse('api_token_auth')  # URL для получения токена

    def test_get_token(self):
        """
        Пользователь может получить токен.
        """
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(self.url_get_token, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_use_token_to_access_protected_endpoint(self):
        """
        Пользователь может использовать токен для доступа к защищенному эндпоинту.
        """
        # Получаем токен
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(self.url_get_token, data, format='json')
        token = response.data['token']

        # Используем токен для доступа к защищенному эндпоинту (например, список постов)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        url = reverse('post-list')  # URL для списка постов (из blogapp)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


from django.test import TestCase
from django.contrib.auth.models import User
from userapp.models import UserProfile

class UserProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.profile = UserProfile.objects.create(user=cls.user, role='reader')

    def test_profile_creation(self):
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.role, 'reader')
        self.assertEqual(str(self.profile), 'testuser (Читатель)')

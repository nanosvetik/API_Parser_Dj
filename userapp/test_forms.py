from django.test import TestCase
from django.contrib.auth.models import User
from userapp.forms import RegisterForm, LoginForm
class RegisterFormTest(TestCase):
    def test_form_valid(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_email(self):
        User.objects.create_user(username='existinguser', email='test@example.com', password='12345')
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['Пользователь с таким email уже существует.'])

class LoginFormTest(TestCase):
    def test_form_valid(self):
        form_data = {
            'username': 'testuser',
            'password': 'testpassword123',
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())
from django.test import TestCase
from blogapp.forms import PostForm
from blogapp.models import Tag
from django.contrib.auth.models import User

class PostFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.tag = Tag.objects.create(name='Python')

    def test_form_valid(self):
        form_data = {
            'title': 'New Post',
            'content': 'This is a new post.',
            'status': 'published',
            'tags': [self.tag.id]
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form_data = {
            'title': '',  # Пустое поле
            'content': 'This is a new post.',
            'status': 'published',
            'tags': [self.tag.id]
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
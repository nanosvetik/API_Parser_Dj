from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from blogapp.models import Post, Tag

class PostViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.tag = Tag.objects.create(name='Python')
        cls.post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            author=cls.user,
            status='published'
        )
        cls.post.tags.add(cls.tag)

    def setUp(self):
        self.client = Client()

    def test_create_post_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('create_post'))
        self.assertEqual(response.status_code, 200)

    def test_inspiration_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('inspiration'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_post_detail_view(self):
        response = self.client.get(reverse('post_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
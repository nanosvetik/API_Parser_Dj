from django.test import TestCase
from blogapp.models import Tag, Post
from django.contrib.auth.models import User

class ModelTestMixin(TestCase):
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

class TagModelTest(ModelTestMixin):
    def test_tag_creation(self):
        self.assertEqual(self.tag.name, 'Python')
        self.assertEqual(str(self.tag), 'Python')

class PostModelTest(ModelTestMixin):
    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.author.username, 'testuser')
        self.assertEqual(self.post.status, 'published')
        self.assertEqual(self.post.tags.count(), 1)
        self.assertEqual(str(self.post), 'Test Post')
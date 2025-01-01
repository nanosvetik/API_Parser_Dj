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

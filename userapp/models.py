from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}: {self.message}"

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('reader', 'Читатель'),
        ('author', 'Автор'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='reader')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    requested_author = models.BooleanField(default=False)  # Новое поле для запроса статуса

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


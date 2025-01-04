from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class PostManager(models.Manager):
    def published(self):
        """
        Возвращает только опубликованные посты.
        """
        return self.filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('moderation', 'На модерации'),
        ('published', 'Опубликовано'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

    # Кастомный менеджер
    objects = PostManager()

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')  # Строковая ссылка на модель Post
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Автор комментария
    content = models.TextField()  # Текст комментария
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    def __str__(self):
        return f'Комментарий от {self.author.username} к посту "{self.post.title}"'
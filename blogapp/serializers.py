# blogapp/serializers.py
from rest_framework import serializers
from .models import Post, Comment, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'  # Включаем все поля модели

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()  # Отображаем имя автора

    class Meta:
        model = Comment
        fields = '__all__'  # Включаем все поля модели

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()  # Отображаем имя автора
    comments = CommentSerializer(many=True, read_only=True)  # Вложенный сериализатор для комментариев
    tags = TagSerializer(many=True, read_only=True)  # Вложенный сериализатор для тегов

    class Meta:
        model = Post
        fields = '__all__'  # Включаем все поля модели
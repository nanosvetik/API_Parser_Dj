# userapp/serializers.py
from rest_framework import serializers
from .models import UserProfile, Notification

class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Отображаем имя пользователя

    class Meta:
        model = Notification
        fields = '__all__'  # Включаем все поля модели

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Отображаем имя пользователя
    notifications = NotificationSerializer(many=True, read_only=True)  # Вложенный сериализатор для уведомлений

    class Meta:
        model = UserProfile
        fields = '__all__'  # Включаем все поля модели
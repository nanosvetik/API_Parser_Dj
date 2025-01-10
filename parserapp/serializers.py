# parserapp/serializers.py
from rest_framework import serializers
from .models import Skill, Vacancy

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'  # Включаем все поля модели

class VacancySerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)  # Вложенный сериализатор для навыков

    class Meta:
        model = Vacancy
        fields = '__all__'  # Включаем все поля модели
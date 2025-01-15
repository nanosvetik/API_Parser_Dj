# parserapp/serializers.py
from rest_framework import serializers
from .models import Vacancy, Skill

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']

class VacancySerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Vacancy
        fields = ['id', 'title', 'description', 'url', 'location', 'experience', 'work_format', 'employment_type', 'skills', 'created_at']



class VacancySearchSerializer(serializers.Serializer):
    profession = serializers.CharField(required=True, help_text="Профессия для поиска вакансий")
    experience = serializers.CharField(required=False, default="noExperience", help_text="Опыт работы")
    work_format = serializers.CharField(required=False, allow_null=True, help_text="Формат работы (удаленно, гибрид, офис)")
    employment_type = serializers.CharField(required=False, allow_null=True, help_text="Тип занятости (полный день, частичная занятость, гибкий график)")
    location = serializers.IntegerField(required=False, default=1, help_text="ID региона")



class HomePageSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    features = serializers.ListField(child=serializers.DictField())


class ContactPageSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    contacts = serializers.ListField(child=serializers.DictField())

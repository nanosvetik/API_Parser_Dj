from django.contrib import admin

from .models import Vacancy, Skill

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'url')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
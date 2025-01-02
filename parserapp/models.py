from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Vacancy(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)  # Разрешить NULL и пустые значения
    url = models.URLField()
    location = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)
    schedule = models.CharField(max_length=255)
    skills = models.ManyToManyField(Skill, related_name='vacancies')

    def __str__(self):
        return self.title
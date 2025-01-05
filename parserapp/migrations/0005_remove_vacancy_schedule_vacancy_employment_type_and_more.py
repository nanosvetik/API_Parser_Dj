# Generated by Django 5.1.4 on 2025-01-05 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parserapp', '0004_vacancy_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacancy',
            name='schedule',
        ),
        migrations.AddField(
            model_name='vacancy',
            name='employment_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='work_format',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
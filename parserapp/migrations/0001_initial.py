# Generated by Django 5.1.4 on 2024-12-21 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('url', models.URLField()),
                ('location', models.CharField(max_length=255)),
                ('experience', models.CharField(max_length=255)),
                ('schedule', models.CharField(max_length=255)),
                ('skills', models.ManyToManyField(related_name='vacancies', to='parserapp.skill')),
            ],
        ),
    ]
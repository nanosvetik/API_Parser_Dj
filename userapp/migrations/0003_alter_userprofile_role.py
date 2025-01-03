# Generated by Django 5.1.4 on 2024-12-28 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0002_remove_userprofile_avatar_remove_userprofile_bio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('reader', 'Читатель'), ('author', 'Автор'), ('moderator', 'Модератор'), ('admin', 'Администратор')], default='reader', max_length=20),
        ),
    ]

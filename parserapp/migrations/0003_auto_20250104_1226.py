from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('parserapp', '0002_alter_vacancy_description'),  # Указываем последнюю миграцию
    ]

    operations = [
        migrations.RunSQL(
            sql='CREATE INDEX idx_vacancy_skills_skill_id ON parserapp_vacancy_skills (skill_id);',
            reverse_sql='DROP INDEX idx_vacancy_skills_skill_id;'
        ),
    ]
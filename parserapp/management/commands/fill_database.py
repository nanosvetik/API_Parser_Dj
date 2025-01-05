# parserapp/management/commands/fill_database.py
import aiohttp
import asyncio
from django.core.management.base import BaseCommand
from django.db import models
from datetime import datetime, timedelta
from asgiref.sync import sync_to_async
from django.db.models import Count
from parserapp.models import Skill, Vacancy

DOMAIN = 'https://api.hh.ru/'
URL_VACANCIES = f'{DOMAIN}vacancies'

class Command(BaseCommand):
    help = 'Заполняет базу данных вакансиями и навыками из API hh.ru'

    def add_arguments(self, parser):
        parser.add_argument('profession', type=str, help='Профессия для поиска вакансий')
        parser.add_argument('--experience', type=str, default='noExperience', help='Опыт работы')
        parser.add_argument('--work_format', type=str, default=None, help='Формат работы (удаленно, гибрид, офис)')  # Новый параметр
        parser.add_argument('--employment_type', type=str, default=None, help='Тип занятости (полный день, частичная занятость, гибкий график)')  # Новый параметр
        parser.add_argument('--location', type=int, default=1, help='ID региона')

    async def fetch_vacancies(self, session, search_text, experience, work_format=None, employment_type=None, location=None):
        vacancies = []
        params = {
            'text': search_text,
            'experience': experience,
            'page': 0,
            'per_page': 50  # Количество вакансий на странице
        }

        # Добавляем новые параметры, если они указаны
        if work_format:
            params['work_format'] = work_format  # Новый параметр
        if employment_type:
            params['employment_type'] = employment_type  # Новый параметр
        if location:
            params['area'] = location

        while True:
            async with session.get(URL_VACANCIES, params=params) as response:
                if response.status != 200:
                    self.stdout.write(self.style.ERROR(f"Ошибка при запросе: {response.status}"))
                    self.stdout.write(self.style.ERROR(f"Ответ API: {await response.text()}"))
                    break

                data = await response.json()
                vacancies.extend(data['items'])

                if params['page'] >= data['pages'] - 1:
                    break

                params['page'] += 1

        self.stdout.write(self.style.SUCCESS(f"Получено {len(vacancies)} вакансий"))
        return vacancies

    async def fetch_vacancy_details(self, session, vacancy_id):
        url = f"{URL_VACANCIES}/{vacancy_id}"
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                self.stdout.write(
                    self.style.ERROR(f"Ошибка при запросе деталей вакансии {vacancy_id}: {response.status}"))
                return None

    async def fetch_multiple_vacancies(self, vacancy_ids):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_vacancy_details(session, vacancy_id) for vacancy_id in vacancy_ids]
            return await asyncio.gather(*tasks)

    @sync_to_async
    def clear_database(self, experience=None):
        """Удаляет вакансии, которые не соответствуют текущему запросу."""
        if experience:
            # Удаляем все вакансии, которые не соответствуют текущему опыту
            Vacancy.objects.exclude(experience=experience).delete()
        else:
            # Удаляем все вакансии, если опыт не указан
            Vacancy.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('База данных очищена от нерелевантных вакансий.'))

    @sync_to_async
    def save_vacancy(self, vacancy, vacancy_detail, top_skills):
        description = vacancy['snippet'].get('responsibility', 'Описание не указано')

        # Извлекаем формат работы и тип занятости
        work_format = vacancy.get('schedule', {}).get('name', 'Не указано')  # Формат работы из поля schedule
        employment_type = vacancy.get('employment', {}).get('name', 'Не указано')  # Тип занятости

        # Проверяем, существует ли вакансия в базе
        vacancy_obj, created = Vacancy.objects.get_or_create(
            url=vacancy['alternate_url'],  # Используем URL как уникальный идентификатор
            defaults={
                'title': vacancy['name'],
                'description': description,
                'location': vacancy.get('area', {}).get('name', 'Не указано'),
                'experience': vacancy.get('experience', {}).get('name', 'Не указано'),
                'work_format': work_format,  # Формат работы
                'employment_type': employment_type,  # Тип занятости
            }
        )

        # Обновляем данные, если вакансия уже существует
        if not created:
            vacancy_obj.title = vacancy['name']
            vacancy_obj.description = description
            vacancy_obj.location = vacancy.get('area', {}).get('name', 'Не указано')
            vacancy_obj.experience = vacancy.get('experience', {}).get('name', 'Не указано')
            vacancy_obj.work_format = work_format  # Формат работы
            vacancy_obj.employment_type = employment_type  # Тип занятости
            vacancy_obj.save()

        # Создаем или получаем навыки из топ-10
        for skill_name in [skill['name'] for skill in vacancy_detail.get('key_skills', [])]:
            if skill_name in top_skills:
                skill, _ = Skill.objects.get_or_create(name=skill_name)
                vacancy_obj.skills.add(skill)

        self.stdout.write(self.style.SUCCESS(f"Сохранена вакансия: {vacancy_obj.title}"))

    async def save_to_database(self, vacancies, search_text):
        skill_counter = {}

        # Приводим поисковый запрос к нижнему регистру и разбиваем на ключевые слова
        keywords = search_text.lower().split()

        # Сначала собираем все навыки и считаем их частоту
        vacancy_ids = [vacancy['id'] for vacancy in vacancies]
        vacancy_details = await self.fetch_multiple_vacancies(vacancy_ids)

        for vacancy, vacancy_detail in zip(vacancies, vacancy_details):
            if not vacancy_detail:
                continue

            # Проверяем, что в названии или описании вакансии есть ключевые слова из запроса
            title = vacancy['name'].lower()
            description = vacancy_detail.get('description', '').lower()

            if not any(keyword in title or keyword in description for keyword in keywords):
                continue  # Пропускаем вакансии, не связанные с запросом

            # Считаем навыки
            key_skills = [skill['name'] for skill in vacancy_detail.get('key_skills', [])]
            for skill_name in key_skills:
                if skill_name in skill_counter:
                    skill_counter[skill_name] += 1
                else:
                    skill_counter[skill_name] = 1

        # Сортируем навыки по частоте упоминания (в порядке убывания)
        sorted_skills = sorted(skill_counter.items(), key=lambda x: x[1], reverse=True)

        # Ограничиваем список топ-10 навыками
        top_skills = [skill[0] for skill in sorted_skills[:10]]

        # Сохраняем вакансии и связываем их с топ-10 навыками
        for vacancy, vacancy_detail in zip(vacancies, vacancy_details):
            if not vacancy_detail:
                continue

            # Проверяем, что в названии или описании вакансии есть ключевые слова из запроса
            title = vacancy['name'].lower()
            description = vacancy_detail.get('description', '').lower()

            if not any(keyword in title or keyword in description for keyword in keywords):
                continue  # Пропускаем вакансии, не связанные с запросом

            await self.save_vacancy(vacancy, vacancy_detail, top_skills)

        # Выводим топ-10 навыков
        self.stdout.write(self.style.SUCCESS("Топ-10 навыков:"))
        for skill_name, count in sorted_skills[:10]:
            self.stdout.write(self.style.SUCCESS(f"{skill_name}: {count} упоминаний"))

    async def handle_async(self, *args, **kwargs):
        profession = kwargs.get('profession')
        experience = kwargs.get('experience', 'noExperience')
        work_format = kwargs.get('work_format', None)
        employment_type = kwargs.get('employment_type', None)
        location = kwargs.get('location', 1)

        if not profession:
            self.stdout.write(self.style.ERROR('Профессия не указана.'))
            return

        # Очищаем базу данных от нерелевантных вакансий
        await self.clear_database(experience=experience)

        async with aiohttp.ClientSession() as session:
            vacancies = await self.fetch_vacancies(session, profession, experience, work_format, employment_type,
                                                   location)
            await self.save_to_database(vacancies, profession)  # Передаем поисковый запрос

    def handle(self, *args, **kwargs):
        asyncio.run(self.handle_async(*args, **kwargs))
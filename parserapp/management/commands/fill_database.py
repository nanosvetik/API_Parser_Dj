import requests
from django.core.management.base import BaseCommand
from parserapp.models import Skill, Vacancy

DOMAIN = 'https://api.hh.ru/'
URL_VACANCIES = f'{DOMAIN}vacancies'

class Command(BaseCommand):
    help = 'Заполняет базу данных вакансиями и навыками из API hh.ru'

    def handle(self, *args, **kwargs):
        search_text = 'QA OR "Инженер по тестированию" OR Тестировщик'
        experience = 'noExperience'
        schedule = 'remote'
        location = 1  # ID региона (1 — Москва)

        # Очищаем базу данных перед новым поиском
        self.clear_database()

        vacancies = self.fetch_vacancies(search_text, experience, schedule, location)
        self.save_to_database(vacancies)
        self.stdout.write(self.style.SUCCESS('Данные успешно сохранены в базу данных!'))

    def clear_database(self):
        """Удаляет все вакансии и навыки из базы данных."""
        Vacancy.objects.all().delete()
        Skill.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('База данных очищена.'))

    def fetch_vacancies(self, search_text, experience, schedule, location=None):
        vacancies = []
        params = {
            'text': search_text,
            'experience': experience,
            'schedule': schedule,
            'area': location,  # Передаём ID региона
            'page': 0,
            'per_page': 50
        }

        while len(vacancies) < 20:
            response = requests.get(URL_VACANCIES, params=params)
            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(f"Ошибка при запросе: {response.status_code}"))
                self.stdout.write(self.style.ERROR(f"Ответ API: {response.text}"))  # Вывод ответа API
                break

            data = response.json()
            vacancies.extend(data['items'])

            if params['page'] >= data['pages'] - 1:
                break

            params['page'] += 1

        self.stdout.write(self.style.SUCCESS(f"Получено {len(vacancies)} вакансий"))
        return vacancies[:20]

    def save_to_database(self, vacancies):
        # Словарь для подсчета частоты навыков
        skill_counter = {}

        # Сначала собираем все навыки и считаем их частоту
        for vacancy in vacancies:
            vacancy_detail = requests.get(f"{URL_VACANCIES}/{vacancy['id']}").json()
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
        for vacancy in vacancies:
            vacancy_detail = requests.get(f"{URL_VACANCIES}/{vacancy['id']}").json()
            key_skills = [skill['name'] for skill in vacancy_detail.get('key_skills', [])]

            # Проверяем и заполняем описание
            description = vacancy['snippet'].get('responsibility', 'Описание не указано')

            # Создаем или получаем вакансию
            vacancy_obj, created = Vacancy.objects.get_or_create(
                title=vacancy['name'],
                description=description,  # Гарантируем, что поле не пустое
                url=vacancy['alternate_url'],
                location=vacancy.get('area', {}).get('name', 'Не указано'),
                experience=vacancy.get('experience', {}).get('name', 'Не указано'),
                schedule=vacancy.get('schedule', {}).get('name', 'Не указано')
            )

            # Создаем или получаем навыки из топ-10
            for skill_name in key_skills:
                if skill_name in top_skills:
                    skill, _ = Skill.objects.get_or_create(name=skill_name)
                    vacancy_obj.skills.add(skill)

            self.stdout.write(self.style.SUCCESS(f"Сохранена вакансия: {vacancy_obj.title}"))

        # Выводим топ-10 навыков
        self.stdout.write(self.style.SUCCESS("Топ-10 навыков:"))
        for skill_name, count in sorted_skills[:10]:
            self.stdout.write(self.style.SUCCESS(f"{skill_name}: {count} упоминаний"))
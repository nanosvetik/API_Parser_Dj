# API_Parser_Dj

## Парсер вакансий с HeadHunter (hh.ru) на Django

Этот проект представляет собой парсер вакансий с сайта HeadHunter (hh.ru) с использованием их публичного API. Парсер собирает информацию о вакансиях на основе заданных параметров (например, должность, локация, опыт работы, график) и сохраняет данные в базу данных Django. Проект также включает веб-интерфейс для поиска вакансий, просмотра статистики и блога с историями пользователей.

## Что было сделано по заданию
**Пагинация**

Добавлена пагинация на странице с результатами поиска вакансий.

Посты в блоге также разбиты на страницы (по 5 штук на странице).

**Шаблонные фильтры**

Использованы фильтры truncatechars для сокращения текста постов и date для форматирования даты.

**Менеджеры моделей**

Добавлен кастомный менеджер для модели Post, который возвращает только опубликованные посты.

**Сигналы**

Реализован сигнал post_save, который автоматически создает профиль пользователя при регистрации.

**Контекстный процессор**

Добавлен контекстный процессор, который передает роль пользователя в контекст всех шаблонов.

## Структура проекта

API_Parser_Dj/  
├── parserapp/                     # Приложение для парсера вакансий  
│   ├── management/  
│   │   └── commands/  
│   │       └── fill_database.py   # Команда для запуска парсера  
│   ├── migrations/                # Миграции базы данных  
│   ├── templates/                 # Шаблоны HTML  
│   ├── __init__.py  
│   ├── admin.py                   # Админка Django  
│   ├── apps.py  
│   ├── forms.py                   # Форма поиска вакансий  
│   ├── models.py                  # Модели Skill и Vacancy  
│   ├── tests.py  
│   ├── urls.py                    # Маршруты приложения  
│   └── views.py                   # Представления (CBV)  
├── blogapp/                       # Приложение для блога  
│   ├── migrations/                # Миграции базы данных  
│   ├── templates/                 # Шаблоны HTML  
│   ├── __init__.py  
│   ├── admin.py                   # Админка Django  
│   ├── apps.py  
│   ├── forms.py                   # Формы для постов  
│   ├── models.py                  # Модели Post и Tag  
│   ├── tests.py  
│   ├── urls.py                    # Маршруты приложения  
│   └── views.py                   # Представления  
├── userapp/                       # Приложение для пользователей  
│   ├── migrations/                # Миграции базы данных  
│   ├── templates/                 # Шаблоны HTML  
│   ├── __init__.py  
│   ├── admin.py                   # Админка Django  
│   ├── apps.py  
│   ├── forms.py                   # Формы регистрации и авторизации  
│   ├── models.py                  # Модель UserProfile  
│   ├── signals.py                 # Сигналы для автоматического создания профиля  
│   ├── context_processors.py      # Контекстный процессор для передачи роли пользователя  
│   ├── tests.py  
│   ├── urls.py                    # Маршруты приложения  
│   └── views.py                   # Представления  
├── API_Parser_Dj/                 # Основной конфигурационный файл проекта  
│   ├── __init__.py  
│   ├── asgi.py  
│   ├── settings.py                # Настройки проекта  
│   ├── urls.py                    # Основные маршруты проекта  
│   └── wsgi.py  
├── manage.py                      # Управление проектом  
├── requirements.txt               # Зависимости проекта  
└── README.md                      # Описание проекта  

## Как запустить проект

1. Установите зависимости:
pip install -r requirements.txt

2. Запустите сервер:
python manage.py runserver

3. Перейдите по адресу http://127.0.0.1:8000/ в браузере.

## Запуск тестов

Для запуска тестов выполните команду:
python manage.py test

Для проверки покрытия кода тестами:
coverage run manage.py test
coverage report


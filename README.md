# Документация проекта "Парсер вакансий HH"

## О проекте

Проект представляет собой веб-приложение для парсинга вакансий с сайта hh.ru. Пользователи могут искать вакансии по различным параметрам, просматривать результаты, анализировать навыки, а также публиковать посты в блоге и общаться с другими пользователями. Проект также предоставляет REST API для интеграции с другими системами и автоматизации процессов.

## Основные функции:

**Парсинг вакансий:**

Поиск вакансий по профессии, опыту работы, формату работы, типу занятости и региону.

Сохранение результатов в базу данных.

Анализ топ-10 навыков, требуемых для вакансий.

**Блог:**

Публикация постов с возможностью модерации.

Комментирование постов.

Управление тегами для постов.

**Личный кабинет:**

Регистрация и авторизация пользователей.

Управление профилем (аватар, роль).

Уведомления о важных событиях (например, одобрение запроса на статус автора).

**FAQ:**

Часто задаваемые вопросы, сгруппированные по категориям.

Возможность добавления новых вопросов администраторами.

## REST API:

API для работы с вакансиями, постами, комментариями, профилями пользователей и FAQ.

Аутентификация через JWT (JSON Web Token).

# Установка и запуск проекта

**Требования**

Python 3.8+

Django 5.1.4

Установленные зависимости из requirements.txt

**Установка**

1. Клонируйте репозиторий:

git clone <ваш-репозиторий>

cd <ваш-проект>

2. Создайте виртуальное окружение:

python -m venv venv

source venv/bin/activate  # Для Linux/MacOS

venv\Scripts\activate     # Для Windows

3. Установите зависимости:

pip install -r requirements.txt

4. Примените миграции:

python manage.py migrate

5. Создайте суперпользователя:

python manage.py createsuperuser

6. Запустите сервер:

python manage.py runserver

7. Откройте браузер и перейдите по адресу:

http://127.0.0.1:8000/


# Проект состоит из нескольких приложений:

1. **parserapp** — приложение для парсинга вакансий и анализа навыков.
Позволяет искать вакансии на hh.ru и сохранять их в базу данных.

Анализирует навыки, требуемые для вакансий, и отображает топ-10 навыков.

Предоставляет API для поиска вакансий и получения списка навыков.

2. **blogapp** — приложение для публикации постов и комментариев.
Пользователи могут публиковать посты, которые проходят модерацию перед публикацией.

Возможность комментирования постов.

API для управления постами и комментариями.

3. **userapp** — приложение для управления пользователями, их профилями и уведомлениями.
Регистрация и авторизация пользователей.

Управление профилем (аватар, роль).

Уведомления о важных событиях (например, изменение роли или одобрение запроса на статус автора).

API для работы с профилями и уведомлениями.

4. **faq** — приложение для часто задаваемых вопросов.
Вопросы и ответы, сгруппированные по категориям.

# API для получения списка вопросов и управления ими.

**REST API**

Проект предоставляет REST API для взаимодействия с данными. API доступен по адресу /api/ и поддерживает следующие эндпоинты:

1. Вакансии:

GET /api/vacancies/ — список всех вакансий.

GET /api/vacancies/<id>/ — детали конкретной вакансии.

POST /api/search/ — поиск вакансий по параметрам (профессия, опыт работы, формат работы, тип занятости, регион).

2. Навыки:

GET /api/skills/ — список всех навыков, отсортированных по популярности.

3. Посты:

GET /api/posts/ — список всех постов.

POST /api/posts/create/ — создание нового поста (доступно авторам и администраторам).

GET /api/posts/<id>/ — детали конкретного поста.

PUT /api/posts/<id>/edit/ — редактирование поста (доступно автору или администратору).

DELETE /api/posts/<id>/edit/ — удаление поста (доступно автору или администратору).

4. Комментарии:

GET /api/comments/ — список всех комментариев.

POST /api/comments/create/ — создание нового комментария.

PUT /api/comments/<id>/edit/ — редактирование комментария (доступно автору или администратору).

DELETE /api/comments/<id>/edit/ — удаление комментария (доступно автору или администратору).

5. Пользователи:

GET /api/profile/ — данные профиля текущего пользователя.

PUT /api/profile/ — обновление профиля (аватар, роль).

GET /api/notifications/ — список уведомлений для текущего пользователя.

6. FAQ:

GET /api/faq/ — список всех вопросов.

POST /api/faq/create/ — создание нового вопроса (доступно администраторам).

GET /api/faq/<id>/ — детали конкретного вопроса.

PUT /api/faq/<id>/ — редактирование вопроса (доступно администраторам).

DELETE /api/faq/<id>/ — удаление вопроса (доступно администраторам).

7. Аутентификация:

POST /api/token/ — получение JWT-токена для аутентификации.

POST /api/token/refresh/ — обновление JWT-токена.

## Примеры запросов к API

Поиск вакансий:

POST /api/search/

{

    "profession": "Python разработчик",

    "experience": "between1And3",

    "work_format": "remote",

    "employment_type": "fullDay",

    "location": 1

}

Создание поста:

POST /api/posts/create/

{

    "title": "Мой первый пост",

    "content": "Это содержимое моего первого поста.",

    "tags": [1, 2]

}

Получение списка уведомлений:

GET /api/notifications/

# Настройки проекта

Основные настройки проекта находятся в файле settings.py:

DEBUG — режим отладки (выключен).

ALLOWED_HOSTS — список разрешенных хостов.

INSTALLED_APPS — список установленных приложений.

DATABASES — настройки базы данных (по умолчанию SQLite).

STATIC_URL и MEDIA_URL — пути к статическим и медиафайлам.

REST_FRAMEWORK — настройки Django REST Framework.

SIMPLE_JWT — настройки JWT-аутентификации.

# Лицензия

Проект распространяется под лицензией MIT. Подробности в файле LICENSE.


# Библиотечный API

## Описание:

REST API-сервер для управления библиотекой.

Проект разработан на Django REST Framework и предоставляет возможности для управления книгами, авторами и пользователями, а также отслеживания выдачи и возврата книг.

Основной функционал:
- регистрация и авторизация пользователей через JWT токены;
- управление книгами;
- управление авторами;
- управление пользователями;
- выдача книг пользователям;
- отслеживание статуса возврата книг;
- проверка доступности книг;
- автоматическая отправка напоминаний пользователям;
- документация API по стандарту OpenAPI.

## Локальная установка и запуск приложения

### 1. Клонирование проекта

```bash
git clone https://github.com/stepanbaidakov/library.git
```

```bash
git clone <repository_url>
cd library
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
```

### Linux / macOS

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Создание файла `.env`

Создайте файл `.env` по примеру `.env.sample`.

Пример:

```env
SECRET_KEY=your_secret_key
DEBUG=True

POSTGRES_DB=library
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

REDIS_HOST=localhost
REDIS_PORT=6379
```

### 5. Выполнение миграций

```bash
python manage.py migrate
```

### 6. Создание администратора

```bash
python manage.py createsuperuser
```

### 7. Запуск сервера

```bash
python manage.py runserver
```

---

## Запуск через Docker

### Создание файла `.env`

Создайте файл `.env` по шаблону `.env.sample`.

### Сборка и запуск

```bash
docker compose up --build
```

### Запуск в фоне

```bash
docker compose up -d
```

### Выполнение миграций

```bash
docker compose exec web python manage.py migrate
```

### Создание суперпользователя

```bash
docker compose exec web python manage.py createsuperuser
```

### Сбор статических файлов

```bash
docker compose exec web python manage.py collectstatic
```

---

##  CI/CD

Workflow расположен в каталоге:

```
.github/workflows/
```

### Необходимые GitHub Secrets

Добавьте в:

```
Settings → Secrets and variables → Actions
```

следующие секреты:

- SERVER_HOST
- SERVER_USER
- SERVER_SSH_KEY

### Что происходит при Push в основную ветку

- Получение актуального кода
- Установка зависимостей
- Запуск тестов
- Сборка Docker-образов
- Подключение к серверу по SSH
- Обновление приложения
- Перезапуск контейнеров
- Автоматический деплой

---

## Деплой на сервер

На сервере должны быть установлены:

- Git
- Docker
- Docker Compose

### Проверка установки:

```bash
git --version
docker --version
docker compose version
```

### Создание файла `.env`:

```bash
nano .env
```

После отправки изменений в основную ветку приложение будет автоматически задеплоено.

---

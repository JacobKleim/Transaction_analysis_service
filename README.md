# Transaction Analysis Service — Django Backend

Мини-сервис для анализа транзакций пользователей с возможностью автоматической категоризации, установки лимитов трат и получения статистики расходов.

---

## 🚀 Возможности

* Импорт транзакций из JSON-файла
* Валидация и автоматическая категоризация транзакций
* Установка и контроль дневных и недельных лимитов расходов
* Асинхронная проверка лимитов с помощью Celery
* REST API для получения статистики по пользователю
* Логирование предупреждений о превышении лимитов

---

## 🔗 Внешние компоненты

* Используется Redis в качестве брокера сообщений для Celery
* База данных — PostgreSQL

---

## 📦 Технологии

* Python 3.12
* Django 5.2.2
* Django REST Framework 3.16.0
* PostgreSQL
* Celery + Redis
* Poetry для управления зависимостями
* Docker + Docker Compose для контейнеризации

---

## ⚙️ Переменные окружения

В файле `.env` должны быть определены:

```env
DJANGO_SECRET_KEY=django-insecure-key
DJANGO_DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=postgres_password
POSTGRES_DB=postgres_db

CELERY_BROKER_URL=redis://redis:6379/0
```

---

## 🐍 Poetry

- Установите pipx и Poetry:
  
   ```bash
   pip install --upgrade pip
   pip install pipx
   pipx install poetry
   ```

- Установка зависимостей:

   ```bash
   poetry install
   ```

---

## 🐳 Docker

- Сборка и запуск контейнеров:

  ```bash
  docker-compose up --build
  ```

- Применение миграций:

  ```bash
  docker-compose exec django python manage.py migrate
  ```

- Импорт транзакций из JSON-файла (management-команда):

  ```bash
  docker-compose exec django python manage.py import_transactions sample_transactions.json
  ```
  *Для удобства можно использовать Makefile с алиасами для этих команд.*

- После запуска сервис будет доступен по адресу:
  ```bash
  http://localhost:8000
  ```

---

## 🔄 Асинхронная проверка лимитов

- После импорта транзакции запускается задача Celery `check_limits_task`.
- Задача проверяет, не превышены ли дневные и недельные лимиты пользователя.
- При превышении лимитов генерируются предупреждения в логах.

---

## 📋 API Endpoints

Получение статистики пользователя(работает с тестовыми данными из `sample_transactions.json`):
  ```
  GET /users/{user_id}/stats/?from=2024-11-01&to=2024-11-03
  ```

Ответ:
```json
{
  "total_spent": 3750.0,
  "by_category": {
      "Food": 2000.0,
      "Transport": 1000.0,
      "Entertainment": 750.0
  },
  "daily_average": 1250.0
}
```

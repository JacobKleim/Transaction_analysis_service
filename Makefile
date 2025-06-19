.PHONY: all

format_all: ## Запуск линтеров
	poetry run ruff format .
	poetry run ruff check --fix .

build_up: ## Собирает(пересобирает) контейнеры и запускает docker-compose
	docker-compose up --build

makemigrations: ## Создаёт новые файлы миграций Django ORM
	docker-compose exec django python manage.py makemigrations

migrate: ## Применяет новые миграции Django ORM
	docker-compose exec django python manage.py migrate

createsuperuser: ## Создаёт суперпользователя
	docker-compose exec django python manage.py createsuperuser

import: ## Импортирует тестовые данные
	docker-compose exec django python manage.py import_transactions sample_transactions.json

down: ## Останавливает и удаляет контейнеры, сети и тома
	docker-compose down -v

help: ## Показывает список доступных команд
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-22s\033[0m %s\n", $$1, $$2}'




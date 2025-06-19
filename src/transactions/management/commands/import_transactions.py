import json
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from transactions.models import Transaction
from transactions.tasks import check_limits_task
from transactions.validators import TransactionValidator

User = get_user_model()

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent


class Command(BaseCommand):
    help = "Импортирует транзакции из JSON-файла"

    def add_arguments(self, parser):
        parser.add_argument(
            "json_file", type=str, help="Путь к JSON-файлу с транзакциями"
        )

    def handle(self, *args, **kwargs):
        json_file = BASE_DIR / kwargs["json_file"]

        try:
            with open(json_file, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.stderr.write(self.style.ERROR(f"Ошибка при чтении файла: {e}"))
            return

        count = 0
        for transaction in data:
            try:
                validator = TransactionValidator(transaction)
                cleaned_data = validator.validate()

                Transaction.objects.create(
                    id=transaction["id"],
                    user=cleaned_data["user"],
                    amount=cleaned_data["amount"],
                    currency=cleaned_data["currency"],
                    category=cleaned_data["category"],
                    description=cleaned_data["description"],
                    timestamp=cleaned_data["timestamp"],
                )
                check_limits_task.delay(
                    transaction["user_id"], transaction["timestamp"]
                )
                count += 1
            except User.DoesNotExist:
                self.stderr.write(
                    self.style.WARNING(
                        f"Пользователь с id={transaction['user_id']} не найден"
                    )
                )
            except IntegrityError:
                self.stderr.write(
                    self.style.WARNING(f"Транзакция {transaction['id']} уже существует")
                )
            except Exception as e:
                self.stderr.write(
                    self.style.ERROR(f"Ошибка при импорте {transaction['id']}: {e}")
                )

        self.stdout.write(self.style.SUCCESS(f"Импортировано {count} транзакций"))

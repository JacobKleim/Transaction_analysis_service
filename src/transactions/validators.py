import logging
from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_datetime
from typing import Any, Dict

from transactions.models import Transaction

User = get_user_model()
logger = logging.getLogger(__name__)


class TransactionValidator:
    """
    Валидатор для проверки и очистки данных транзакции.
    """
    def __init__(self, data: dict) -> None:
        """
        :param data: словарь с данными транзакции
        """
        self.data = data
        self.cleaned_data = {}

    def validate(self) -> Dict[str, Any]:
        """
        Валидирует все поля транзакции и возвращает очищенные данные.
        """
        logger.info(f"Валидация транзакции: {self.data}")
        self._validate_required_fields()
        self._validate_user()
        self._validate_currency()
        self._validate_amount()
        self._validate_timestamp()
        self._validate_category()
        self._validate_description()
        logger.info(f"Валидация успешна: {self.cleaned_data}")
        return self.cleaned_data

    def _validate_required_fields(self) -> None:
        """
        Проверяет наличие обязательных полей.
        """
        required = ["id", "user_id", "amount", "currency", "timestamp"]
        missing = [f for f in required if f not in self.data]
        if missing:
            logger.error(f"Отсутствуют обязательные поля: {missing}")
            raise ValueError(f"Отсутствуют обязательные поля: {missing}")

    def _validate_user(self) -> None:
        """
        Проверяет существование пользователя.
        """
        try:
            user = User.objects.get(id=self.data["user_id"])
        except User.DoesNotExist:
            logger.error(f"Пользователь с id={self.data['user_id']} не найден")
            raise ValueError(f"Пользователь с id={self.data['user_id']} не найден")
        self.cleaned_data["user"] = user

    def _validate_currency(self) -> None:
        """
        Проверяет корректность валюты.
        """
        currency = self.data.get("currency")
        if currency not in Transaction.Currency.values:
            logger.error(f"Неподдерживаемая валюта: {currency}")
            raise ValueError(f"Неподдерживаемая валюта: {currency}")
        self.cleaned_data["currency"] = currency

    def _validate_amount(self) -> None:
        """
        Проверяет корректность суммы.
        """
        try:
            amount = float(self.data.get("amount"))
        except (ValueError, TypeError):
            logger.error(f"Некорректное значение amount: {self.data.get('amount')}")
            raise ValueError(f"Некорректное значение amount: {self.data.get('amount')}")
        self.cleaned_data["amount"] = amount

    def _validate_timestamp(self) -> None:
        """
        Проверяет корректность даты и времени.
        """
        timestamp = parse_datetime(self.data.get("timestamp"))
        if not timestamp:
            logger.error(f"Некорректный формат даты: {self.data.get('timestamp')}")
            raise ValueError(f"Некорректный формат даты: {self.data.get('timestamp')}")
        self.cleaned_data["timestamp"] = timestamp

    def _validate_category(self) -> None:
        """
        Проверяет и определяет категорию транзакции.
        """
        category = self.data.get("category")
        description = self.data.get("description", "")
        if category not in Transaction.Category.values:
            from transactions.utils import auto_categorize
            category = auto_categorize(description)
        self.cleaned_data["category"] = category

    def _validate_description(self) -> None:
        """
        Добавляет описание транзакции.
        """
        self.cleaned_data["description"] = self.data.get("description", "")

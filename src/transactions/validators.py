from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_datetime

from transactions.models import Transaction

User = get_user_model()


class TransactionValidator:
    def __init__(self, data: dict):
        self.data = data
        self.cleaned_data = {}

    def validate(self):
        self._validate_required_fields()
        self._validate_user()
        self._validate_currency()
        self._validate_amount()
        self._validate_timestamp()
        self._validate_category()
        self._validate_description()
        return self.cleaned_data

    def _validate_required_fields(self):
        required = ["id", "user_id", "amount", "currency", "timestamp"]
        missing = [f for f in required if f not in self.data]
        if missing:
            raise ValueError(f"Отсутствуют обязательные поля: {missing}")

    def _validate_user(self):
        try:
            user = User.objects.get(id=self.data["user_id"])
        except User.DoesNotExist:
            raise ValueError(f"Пользователь с id={self.data['user_id']} не найден")
        self.cleaned_data["user"] = user

    def _validate_currency(self):
        currency = self.data.get("currency")
        if currency not in Transaction.Currency.values:
            raise ValueError(f"Неподдерживаемая валюта: {currency}")
        self.cleaned_data["currency"] = currency

    def _validate_amount(self):
        try:
            amount = float(self.data.get("amount"))
        except (ValueError, TypeError):
            raise ValueError(f"Некорректное значение amount: {self.data.get('amount')}")
        self.cleaned_data["amount"] = amount

    def _validate_timestamp(self):
        timestamp = parse_datetime(self.data.get("timestamp"))
        if not timestamp:
            raise ValueError(f"Некорректный формат даты: {self.data.get('timestamp')}")
        self.cleaned_data["timestamp"] = timestamp

    def _validate_category(self):
        category = self.data.get("category")
        description = self.data.get("description", "")
        if category not in Transaction.Category.values:
            from transactions.utils import auto_categorize

            category = auto_categorize(description)
        self.cleaned_data["category"] = category

    def _validate_description(self):
        self.cleaned_data["description"] = self.data.get("description", "")

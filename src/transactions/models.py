from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Transaction(models.Model):
    """Модель транзакции."""

    class Category(models.TextChoices):
        FOOD = "Food", "Еда"
        TRANSPORT = "Transport", "Транспорт"
        ENTERTAINMENTS = "Entertainment", "Развлечения"
        UTILITIES = "Utilities", "Коммунальные услуги"
        OTHER = "Other", "Другое"

    class Currency(models.TextChoices):
        RUB = "RUB", "Рубль"
        USD = "USD", "Доллар США"
        EUR = "EUR", "Евро"

    id = models.CharField(max_length=50, primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name="Пользователь",
    )
    amount = models.FloatField(
        verbose_name="Сумма",
    )
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.RUB,
        verbose_name="Валюта",
    )
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER,
        verbose_name="Категория",
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    timestamp = models.DateTimeField(verbose_name="Дата и время", db_index=True)

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"
        indexes = [
            models.Index(fields=["user", "timestamp"], name="ix_user_timestamp"),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.amount} {self.get_currency_display()} ({self.get_category_display()})"

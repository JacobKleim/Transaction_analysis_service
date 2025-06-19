from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя, которую позже можно будет расширить дополнительными полями."""

    daily_limit = models.FloatField(default=5000, verbose_name="Дневной лимит трат")
    weekly_limit = models.FloatField(default=35000, verbose_name="Недельный лимит трат")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

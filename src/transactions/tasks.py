import logging
from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.utils.dateparse import parse_datetime

from .models import Transaction

logger = logging.getLogger(__name__)

User = get_user_model()


@shared_task
def check_limits_task(user_id: int, raw_date: str) -> None:
    """
    Асинхронная задача для проверки превышения дневных и недельных лимитов пользователя.
    :param user_id: ID пользователя
    :param raw_date: дата транзакции (строка)
    """
    logger.info(f"Запуск проверки лимитов для пользователя {user_id} на дату {raw_date}")
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        logger.error(f"Пользователь с id={user_id} не найден для проверки лимитов")
        return

    date = parse_datetime(raw_date).date()

    # === ДНЕВНОЙ ЛИМИТ ===
    daily_expenses = Transaction.objects.filter(
        user_id=user_id,
        timestamp__date=date,
        amount__lt=0,
    )
    daily_total = daily_expenses.aggregate(Sum("amount"))["amount__sum"] or 0

    if abs(daily_total) > user.daily_limit:
        logger.warning(
            f"Пользователь {user_id} превысил дневной лимит на {date}: {abs(daily_total)} > {user.daily_limit}"
        )

    # === НЕДЕЛЬНЫЙ ЛИМИТ ===
    start_of_week = date - timedelta(days=date.weekday())  # Понедельник
    end_of_week = start_of_week + timedelta(days=6)

    weekly_expenses = Transaction.objects.filter(
        user_id=user_id,
        timestamp__date__range=(start_of_week, end_of_week),
        amount__lt=0,
    )
    weekly_total = weekly_expenses.aggregate(Sum("amount"))["amount__sum"] or 0

    if abs(weekly_total) > user.weekly_limit:
        logger.warning(
            f"Пользователь {user_id} превысил недельный лимит ({start_of_week} – {end_of_week}): {abs(weekly_total)} > {user.weekly_limit}"
        )
    logger.info(f"Проверка лимитов для пользователя {user_id} завершена")

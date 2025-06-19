from datetime import datetime, time, timedelta

from django.db.models import Sum
from django.utils import timezone

from transactions.models import Transaction


def get_user_stats(user_id, from_date, to_date):
    start_dt = timezone.make_aware(datetime.combine(from_date, time.min))
    end_dt = timezone.make_aware(datetime.combine(to_date + timedelta(days=1), time.min))

    transactions = Transaction.objects.filter(timestamp__gte=start_dt, timestamp__lt=end_dt, user_id=user_id)
    expenses = transactions.filter(amount__lt=0)

    total_spent = expenses.aggregate(total=Sum("amount"))["total"] or 0

    by_category = {}
    for category in Transaction.Category.choices:
        category_total = expenses.filter(category=category[0]).aggregate(total=Sum("amount"))["total"] or 0
        if category_total:
            by_category[category[0]] = abs(category_total)

    delta_days = (to_date - from_date).days + 1
    daily_average = abs(total_spent) / delta_days

    return {
        "total_spent": abs(total_spent),
        "by_category": by_category,
        "daily_average": round(daily_average, 2),
    }

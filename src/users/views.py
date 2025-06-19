from django.utils.dateparse import parse_date
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
import logging
from .services import get_user_stats

logger = logging.getLogger(__name__)


class UserStatsView(APIView):
    """
    View для получения статистики пользователя по расходам за период.
    """
    def get(self, request: Request, id: int) -> Response:
        """
        Возвращает статистику расходов пользователя за указанный период.
        Параметры: from (дата), to (дата)
        """
        logger.info(f"Получен запрос статистики для пользователя {id}")
        from_date = parse_date(request.GET.get("from"))
        to_date = parse_date(request.GET.get("to"))
        stats = get_user_stats(id, from_date, to_date)
        logger.info(f"Отправка статистики для пользователя {id}: {stats}")
        return Response(stats)

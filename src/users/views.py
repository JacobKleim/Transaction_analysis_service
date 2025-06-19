from django.utils.dateparse import parse_date
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import get_user_stats


class UserStatsView(APIView):
    def get(self, request, id):
        from_date = parse_date(request.GET.get("from"))
        to_date = parse_date(request.GET.get("to"))

        stats = get_user_stats(id, from_date, to_date)
        return Response(stats)

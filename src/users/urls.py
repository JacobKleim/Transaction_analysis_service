from django.urls import path

from .views import UserStatsView

urlpatterns = [
    path("stats/<int:id>/", UserStatsView.as_view()),
]

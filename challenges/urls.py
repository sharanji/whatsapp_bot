from django.urls import path
from . import views

urlpatterns = [
    path('<int:month>', views.monthlyChallengesBynumber),
    path('<str:month>', views.monthlyChallenges, name="getMonthlyChallenge"),
    path('', views.home),
]

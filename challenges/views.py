from calendar import month
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

# Create your views here.
monthly_challenges = {"January": "quit consuming added sugar",
                      "February": " Spread the Love", "March": "Save $500 in the next 30 days",
                      "April": "Earn an extra $1000 in the next 30 days",
                      "May": "Pay off a certain bill",
                      "June": "Stop shopping online",
                      "July": "Exercise for 20 minutes",
                      "August": "Walk one mile",
                      "September": "Walk one mile",
                      "October": "Go to the gym every day",
                      "November": "Start a gratitude journal",
                      "December": "Do something that makes it impossible to feel sorry for yourself"
                      }


def home(request):
    data = render(request, 'home.html', {
        'months': list(monthly_challenges.keys())})
    return HttpResponse(data)


def monthlyChallengesBynumber(request, month):

    if month > len(monthly_challenges) or month <= 0:
        return HttpResponseNotFound("Invalid month")

    redirect_month = list(monthly_challenges.keys())[month-1]
    redirect_url = reverse("getMonthlyChallenge", args=[redirect_month])
    return HttpResponseRedirect(redirect_url)


def monthlyChallenges(request, month):

    try:
        challenge_text = monthly_challenges[month]
        data = render(request, 'chanallenges.html', {
                      'challenge_text': challenge_text,
                      'month_name': month})
        return HttpResponse(data)
    except:
        return HttpResponseNotFound("Invalid month")

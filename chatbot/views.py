from django.http import HttpResponse
from django.shortcuts import render
from chatbot.botfiles import chat as bot
from datetime import date
from django.views.decorators.clickjacking import xframe_options_exempt


# Create your views here.


@xframe_options_exempt
def getChatUi(request):
    htmlData = render(request, "chatbot.html", {
        'nowDate': date.today(),
    })
    return HttpResponse(htmlData)


def sendChatResponse(request):
    getData = request.GET
    botresponse = bot.talk(getData['question'])
    return HttpResponse(botresponse)

import requests
import json

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

from chatbot.botfiles import chat as bot
from datetime import date

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from .models import *
from .serializers import *




# Create your views here.


def getChatUi(request):
    htmlData = render(request, "chatbot.html", {
        'nowDate': date.today(),
    })
    return HttpResponse(htmlData)

@api_view(['GET'])
def sendChatResponse(request):
    getData = request.GET
    botresponse = bot.talk(getData['question'])
    return Response(botresponse)

fb_version = 'v15.0'
phone_id = '918610711834'
sender_id = '103249319357540'
access_token = 'EAAIe4hYZADdkBAHPCnS3mDeYZBZA37syQV6EJVHZCacgaGNmIzj9wHNloK0wjgZB6cZCgxhu169H8Uhfvt3TkEcIxeWj3gbiFDy2fyHKK7SiFEISNEH28hZCNdTW7gLUZAfxyYhjIZCwY1b2kcaBrJcn6nCRBoeECERDHAZC1gi1ZCDEVjkqqklCvSHBq1W6HOwjKGWMEZCrM8wY1QZDZD'

def GetUserInput(jsonData)->str:
    # try :
        if jsonData['entry'][0]['changes'] :
            changes = jsonData['entry'][0]['changes'][0]
            
            if changes['field'] and changes['field'] == 'messages' :
                getUserinput,user_number =  changes['value']['messages'][0]['text']['body'], changes['value']['contacts'][0]['wa_id']
                user_name = changes['value']['contacts'][0]['profile']['name']
                
                botresponse = bot.talk(getUserinput)
               

                if len(botresponse) == 1:
                    currentquery = chatHistory.objects.filter(contact_number=user_number).last()
                    historySerialiser = ChatHistorySerializer(currentquery, many=False)
                    
                    if historySerialiser.data :
                        responseQueryset = chatResponses.objects.filter(section_name=historySerialiser.data['bot_response']).last()
                        serializer = ChatResponsesSerializer(responseQueryset, many=False)
                    else :
                         
                        responseQueryset = chatResponses.objects.filter(section_name='greeting').last()
                        serializer = ChatResponsesSerializer(responseQueryset, many=False)
                        data = {
                            'customer_query' : getUserinput,
                            'bot_response' : 'service',
                            "contact_number" :user_number,
                        }
                        historySerialiser = ChatHistorySerializer(data=data)
                        if historySerialiser.is_valid():
                            historySerialiser.save()
                    
                else :
                    responseQueryset = chatResponses.objects.filter(section_name=botresponse).last()
                    serializer = ChatResponsesSerializer(responseQueryset, many=False)
                
                jResponse = json.loads(serializer.data['responses'])

                for convo in jResponse :
                    
                    if '<user_name>' in convo:
                        convo = convo.replace('<user_name>', user_name, 1)

                    if 'forwa' in convo :
                        data = {
                            'message' :convo,
                            'contact_number' : user_number,
                        }
                        serializer = CustomerRequestsSerializer(data=data)
                        if serializer.is_valid():
                            serializer.save()
                    
                    url = f"https://graph.facebook.com/{fb_version}/{sender_id}/messages"
                    
                    data = {
                        "messaging_product": "whatsapp",
                        "to": user_number,
                        "type": "text",
                        "text": {
                            "body" :convo,
                        }
                    }
                    headers = {
                        'Content-type': 'application/json',
                        'Authorization':f'Bearer {access_token}',

                    }
                    r = requests.post(url, data=json.dumps(data), headers=headers).json()

                return r
    # except :
    #     return {'message':'An error '}
    
    # return {'message':'Not an user message'}




@api_view(['GET','POST',])
def chatHook(request):
    if request.method == 'GET':

        getData = request.GET

        token = 'jesper@123'

        if(getData['hub.mode'] == 'subscribe' and getData['hub.verify_token'] == token):
            return Response(getData['hub.challenge'])

    r =  GetUserInput(request.data)
    return Response(r, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def getChatHooks(request):
    queryset = MessageHook.objects.all().order_by('-timestamp')
    serializer = MessageHookSerializer(queryset, many=True)

    return Response(serializer.data, status=200)

@api_view(['GET'])
def getCustomerRequest(request):
    queryset = CustomerRequests.objects.all().order_by('-timestamp')
    serializer = CustomerRequestsSerializer(queryset, many=True)

    return Response(serializer.data, status=200)


@api_view(['GET','POST','PUT','DELETE'])
def getchatHistory(request):
    if not request.data:
        queryset = chatResponses.objects.all().order_by('-timestamp')
        serializer = ChatResponsesSerializer(queryset, many=True)

        return Response(serializer.data, status=200)

    else :
        data = {
            "responses_id": request.data['responses_id'],
            "responses": json.dumps(request.data['responses']),
            "section_name": request.data['section_name']
        }
        serializer = ChatResponsesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        else :
            return Response(serializer.errors,status=400)

# url = f"https://graph.facebook.com/{fb_version}/{sender_id}/messages"
                
# data = {
#     "messaging_product": "whatsapp",
#     "recipient_type": "individual",
#     "to": user_number,
#     "type": "text",
#     "text": {
#         "preview_url": True,
#         "body" :botresponse['response'],
#     }
# }

# headers = {
#     'Content-type': 'application/json',
#     'Authorization':f'Bearer {access_token}',
# }

# r = requests.post(url, data=json.dumps(data), headers=headers).json()
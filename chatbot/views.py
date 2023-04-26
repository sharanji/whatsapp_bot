import requests
import json
import time

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

from chatbot.botfiles import chat as bot
from datetime import date

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from heyoo import WhatsApp

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
    return Response(botresponse['response'])

fb_version = 'v16.0'
phone_id = '918610711834'
sender_id = '103249319357540'
# access_token = 'EAAIe4hYZADdkBANUE0Dm0Q90zwd5LqVJjO08jrn6ZCZCUB0uICoi4pgMHZA8E6ayHbVrtSvRrkilz4c5VTZAJZCUoRzSjBI61TRP3gMPPtI8bxxuYBgsBa4vlEWDCn3A48Ynzu4K6zXdL08otA57Mnszs4jWnRJ51jGOgThZAaPoo5MgDZAZBbLcz'
access_token = 'EAAIe4hYZADdkBAOtRew612rP4wTYuxrnH190DZCS8VtL9YBP3mORR44nGczAWwnXbQ4Ca0u6TxZCPfrr1S9Cxw8pue6WHQDmTnIpHhc4ADwmBpjkjQfTe60AQUr1OnITAzZAVnKgA9SUBNrVevlZAkOfpAF2fdkvUqkeezfMDybZBkZCjQlTsUeZAoZAzxO8AuuwGSbD69jjglwZDZD'
php_url ='http://localhost/whatsapp_crm/ajaxSendMessage'#

def GetUserInput(jsonData)->str:
        messenger = WhatsApp(access_token,  phone_number_id=sender_id)
       
        if jsonData['entry'][0]['changes'] :
            changes = jsonData['entry'][0]['changes'][0]
            
            if changes['field'] and changes['field'] == 'messages' :
                try :
                    getUserinput,user_number =  messenger.get_message(jsonData), messenger.get_mobile(jsonData)
                    user_name = messenger.get_name(jsonData)
                except :
                    getUserinput,user_number =  changes['value']['messages'][0]['interactive']['list_reply']['id'], changes['value']['contacts'][0]['wa_id']
                    user_name = messenger.get_name(jsonData)
              
                botresponse = bot.talk(getUserinput)
                sayMenu = False

                if '<user_name>' in botresponse['response']:
                    botresponse['response'] = botresponse['response'].replace('<user_name>', user_name, 1)
                    sayMenu = True


                if 'forward' in botresponse['response'] :
                    data = {
                        'message' :getUserinput,
                        'contact_number' : user_number,
                    }
                    serializer = CustomerRequestsSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                
                if botresponse['type'] == "button":
                    r = messenger.send_button(button=botresponse['response'], recipient_id=user_number,)
                else:
                    r = messenger.send_message(botresponse['response'],user_number,preview_url=True,)

                c = requests.post(php_url,data={
                        'message' : str(getUserinput),
                        'recipient_id' :user_number,
                        'user_name' : user_name,
                        'flag' :1
                    })  
                
                cc = requests.post(php_url,data={
                        'message' : str(botresponse['response']),
                        'recipient_id' :user_number,
                        'user_name' : user_name,
                        'flag' :0
                    })  


                if sayMenu :
                    b = bot.talk('menu')
                    messenger.send_button(button=b['response'], recipient_id=user_number,)
                    

                return r,c,cc
                

    # except :
    #     return {'message':'An error '}
    
    # return {'message':'Not an user message'}




@api_view(['GET','POST',])
def chatHook(request):
    if request.method == 'GET':

        getData = request.GET

        token = 'jesper@123'

        if(request.GET.get('hub.mode') == 'subscribe' and request.GET.get('hub.verify_token') == token):
            return HttpResponse(request.GET.get('hub.challenge'), status=status.HTTP_200_OK)
        else:
            return Response({'meesage':'Unauthorized'},status=401)


    r =  GetUserInput(request.data)
    return Response(r, status=status.HTTP_200_OK)


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
        
@api_view(['GET'])
def deleteCustomerRequests(request):
    queryset = CustomerRequests.objects.all().delete()
    return Response({'message':'Deleted'})


@api_view(['GET','POST',])
def sendMessage(request):
    if request.method == 'POST':

        getData = request.POST
        messenger = WhatsApp(access_token,  phone_number_id=sender_id)
        r = messenger.send_message(getData['message'],getData['number'],preview_url=True,)

        return Response(r, status=status.HTTP_200_OK)
    else:
        return Response({'message':'Get method not available'})
    

@api_view(['GET','POST',])
def sendMessageresponse(request):
    c = requests.post(php_url,data={
                'message' : 'you should tell me',
                'recipient_id' :'918610711834',
                'user_name' : 'sharanji',
            })  
   
    return Response(c.content)



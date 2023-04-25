from django.urls import path
from . import views


urlpatterns = [
    path('talk', views.getChatUi),
    path('talk/ajax', views.sendChatResponse),
    path('chathook', views.chatHook),
    path('getHooks', views.getChatHooks),
    path('getCustomerRequests', views.getCustomerRequest),
    path('getchatHistory', views.getchatHistory),
    path('deleteCustomerRequests', views.deleteCustomerRequests),
    path('sendMessageresponse', views.sendMessageresponse),
    path('sendMessage', views.sendMessage),
]
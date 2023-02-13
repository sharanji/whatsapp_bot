from django.urls import path
from . import views


urlpatterns = [
    path('talk', views.getChatUi),
    path('talk/ajax', views.sendChatResponse),
]

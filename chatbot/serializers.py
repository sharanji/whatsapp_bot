from rest_framework import serializers
from .models import *

class MessageHookSerializer(serializers.ModelSerializer):
    class Meta:
        ordering = ('id',)
        model = MessageHook
        fields = "__all__"

class CustomerRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerRequests
        fields = "__all__"

class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = chatHistory
        fields = "__all__"

class ChatResponsesSerializer(serializers.ModelSerializer):
    class Meta:
        model = chatResponses
        fields = "__all__"
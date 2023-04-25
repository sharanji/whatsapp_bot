# todo/todo_api/models.py
from django.db import models
from django.contrib.auth.models import User

class MessageHook(models.Model):
    messagehook = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)

    def __str__(self):
        return self.messagehook

class CustomerRequests(models.Model):
    message = models.TextField()
    contact_number = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)

    def __str__(self):
        return f"{self.message} -- {self.contact_number}"

class chatHistory(models.Model):
    customer_query = models.TextField()
    bot_response = models.TextField()
    contact_number = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)

    def __str__(self):
        return f"{self.customer_query} -- {self.contact_number}"

class chatResponses(models.Model):
    responses_id = models.TextField()
    responses = models.TextField()
    section_name = models.TextField()
    int_id =  models.TextField(blank = True)
    timestamp = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)

    def __str__(self):
        return f"{self.section_name} --"
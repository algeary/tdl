from django.db import models
from django.contrib.auth.models import User
from django import forms
# Create your models here.


class Task(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    due_date =  models.DateField(null=True, blank=True) # models.DateTimeField(auto_now_add=True, null=True)
    created_location = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    completed_time = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    priority_level = models.CharField(max_length=200,null=True, blank=True) # models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        order_with_respect_to = 'user'

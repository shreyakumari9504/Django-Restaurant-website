from django.utils import timezone
from django.db import models
from datetime import date


# Create your models here.

class enquiry_table(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date = models.DateTimeField(default=timezone.now) 
    time = models.DateTimeField(default=timezone.now)  
    people = models.IntegerField(default=0)
    message = models.TextField()
    subject = models.CharField(max_length=255)


    def __str__(self):
        return self.name
    
class enquiry_table_1(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date = models.DateTimeField(default=timezone.now) 
    time = models.DateTimeField(default=timezone.now)  
    people = models.IntegerField(default=0)
    message = models.TextField()
    subject = models.CharField(max_length=255)


    def __str__(self):
        return self.name
from django.db import models

# Create your models here.

class JSONRecieved(models.model):
    key = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    riskIndex = models.CharField(max_length=200)
    color = models.CharField(max_length=200)
    shape = models.CharField(max_length=200)

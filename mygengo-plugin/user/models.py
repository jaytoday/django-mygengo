from datetime import datetime
from django.db import models

class APIKey(models.Model):
    username = models.CharField(max_length=200)
    public_key = models.CharField(max_length=200)
    private_key = models.CharField(max_length=200)

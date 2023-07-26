from django.db import models
from datetime import datetime

# Create your models here.
class Flash_news(models.Model):
    title=models.CharField(max_length=200)
    description=models.CharField(max_length=1500)
    source=models.CharField(max_length=200)
    sentiment = models.CharField(max_length=255, null=True) 
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title
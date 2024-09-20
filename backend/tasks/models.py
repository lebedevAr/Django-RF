from django.db import models
from django.db.models import TextField


# Create your models here.


class Task(models.Model):
    title = models.TextField(max_length=2500)
    description = models.TextField(max_length=2500, blank=True)
    completed = models.BooleanField(default=False)


from django.db import models
import datetime
import django.utils.timezone
# Create your models here.
class PopUser(models.Model):
    """User model class."""

    username = models.CharField(unique=True, max_length=100)
    password = models.CharField(null=True, max_length=100)
    email = models.CharField(null=True, max_length=100)
    active = models.BooleanField(default=True)
    join_date = models.DateTimeField(auto_now_add=True)


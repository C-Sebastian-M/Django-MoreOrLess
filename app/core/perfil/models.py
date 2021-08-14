from django.conf.global_settings import MEDIA_URL
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

from config.settings import STATIC_URL
class user(models.Model):

    def __str__(self):
        return self


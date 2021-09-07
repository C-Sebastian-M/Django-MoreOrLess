from django.db import models
from config.settings import MEDIA_URL, STATIC_URL

# Create your models here.
from core.registro.models import RegistroUsuario


class PerfilModel(models.Model):
     def __str__(self):
         return self







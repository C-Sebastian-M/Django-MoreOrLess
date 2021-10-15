import uuid

from django.contrib.auth.models import AbstractUser
from config.settings import MEDIA_URL, STATIC_URL
from django.db import models

# Create your models here.

#Modelo de la base de datos, llamando a la clase Abstract user para el registro de usuarios dada por Django
class RegistroUsuario(AbstractUser):
    image = models.ImageField(upload_to='perfil/%Y/%m/%d', null=True, blank=True)
    token = models.UUIDField(primary_key=False,editable=False, null=True, blank=True)

    #Función para obtener la imagen estandar si el usuario no sube una
    def get_image(self):
        if self.image:
            return "{}{}".format(MEDIA_URL, self.image)
        return "{}{}".format(STATIC_URL, 'img/imagen-perfil-sin-foto.png')

import uuid

from django.contrib.auth.models import AbstractUser
from config.settings import MEDIA_URL, STATIC_URL
from django.db import models

# Create your models here.


class RegistroUsuario(AbstractUser):
    image = models.ImageField(upload_to='perfil/%Y/%m/%d', null=True, blank=True)
    token = models.UUIDField(primary_key=False,editable=False, null=True, blank=True)

    def get_image(self):
        if self.image:
            return "{}{}".format(MEDIA_URL, self.image)
        return "{}{}".format(STATIC_URL, 'img/imagen-perfil-sin-foto.png')

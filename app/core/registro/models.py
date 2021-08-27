
from django.contrib.auth.models import AbstractUser
from django.db import models
from config.settings import STATIC_URL, MEDIA_URL

# Create your models here.


class RegistroUsuario(AbstractUser):
    image = models.ImageField(upload_to='perfil/%Y/%m/%d', null=True, blank=True)

    def get_image(self):
        if self.image:
            return "{}{}".format(MEDIA_URL, self.image)
        return "{}{}".format(STATIC_URL,'img/imagen-perfil-sin-foto.png')

    def get_email(self):
        return self.email


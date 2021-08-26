from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Create your models here.
from config.settings import MEDIA_URL, STATIC_URL


class Registro(AbstractUser):
    image = models.ImageField(upload_to='avatar/%y/%m/%d', null=True, blank=True)

    def get_image(self):
        if self.image:
            return "{}{}".format(MEDIA_URL, self.image)
        return "{}{}".format(STATIC_URL, 'img/imagen-perfil-sin-foto.png')

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def get_email(self):
        return self.email



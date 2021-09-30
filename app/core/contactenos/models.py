from django.db import models


# Create your models here.

class ContactUs(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    email = models.EmailField(max_length=50, verbose_name='Correo electronico', unique=True)
    message = models.TextField(max_length=2000, verbose_name="Mensaje")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactenos'
        ordering = ['id']
from django.db import models
from datetime import datetime

class User(models.Model):
    names = models.CharField(max_length=20, verbose_name='Nombres')
    last_names = models.CharField(max_length=20, verbose_name='Apellido')
    date_joined = models.DateField(default=datetime.now(), verbose_name='Fecha de registro')
    avatar = models.ImageField(upload_to='avatar/%y/%m/d', null=True, blank=True)

    def __str__(self):
        return self.names

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        db_table = 'usuario'
        ordering = ['id']









# Create your models here.

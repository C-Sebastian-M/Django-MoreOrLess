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

class presupuesto(models.Model):
    date = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    amount = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Monto')
    category = models.CharField(max_length=50, verbose_name='Categoria')

    def __str__(self):
        return self.date


class gastos(models.Model):
    date = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    amount = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Monto')
    category = models.CharField(max_length=50, verbose_name='Categoria')

    def __str__(self):
        return self.date


class metas(models.Model):
    f_c_m = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    valor = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Monto')
    category = models.CharField(max_length=50, verbose_name='Categoria')

    def __str__(self):
        return self.f_c_m


# Create your models here.

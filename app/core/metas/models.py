from datetime import datetime

from django.db import models

# Create your models here.

class Metas(models.Model):
    f_c_m = models.DateField(verbose_name='Fecha de registro')
    valor = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Monto')
    category = models.CharField(max_length=50, verbose_name='Categoria')
    date = models.DateField(default=datetime.now, verbose_name='Fecha de inicio')

    def __str__(self):
        return self.f_c_m
    class Meta:
        verbose_name = 'Meta'
        verbose_name_plural = 'Metas'
        db_table = 'meta'
        ordering = ['id']
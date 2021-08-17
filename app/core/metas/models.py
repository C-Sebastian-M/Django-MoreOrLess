from datetime import datetime

from django.db import models
from core.categorias.models import Categoria
# Create your models here.



class Metas(models.Model):
    f_c_m = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    amount = models.FloatField('Monto', blank=True, default=None, null=True)
    category = models.ForeignKey(Categoria, blank=True, null=True, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True, verbose_name='Fecha de inicio')

    def __str__(self):
        return self.f_c_m
    class Meta:
        verbose_name = 'Meta'
        verbose_name_plural = 'Metas'
        db_table = 'meta'
        ordering = ['id']
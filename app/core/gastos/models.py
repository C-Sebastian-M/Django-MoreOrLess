from datetime import datetime
from django.db import models

# Create your models here.
from django.forms import model_to_dict

from core.categorias.models import Categoria


class Gastos(models.Model):
    date = models.DateField(auto_now=True, verbose_name='Fecha de registro')
    amount = models.FloatField('Monto', blank=True, default=None, null=True)
    category = models.ForeignKey(Categoria, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.date

    def toJson(self):
        item = model_to_dict(self)

        return item

    class Meta:
        verbose_name = 'Gastos'
        verbose_name_plural = 'Gastos'
        db_table = 'gastos'
        ordering = ['id']
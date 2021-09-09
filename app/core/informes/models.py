from django.db import models


# Create your models here.
from django.forms import model_to_dict

from core.categorias.models import Categoria


class informes(models.Model):
    gastos = models.FloatField('Gasto', blank=True, default=None, null=True)
    presupuesto = models.FloatField('presupuesto', blank=True, default=None, null=True)
    date = models.DateField(auto_now=True, verbose_name='Fecha de registro')
    semana = models.FloatField('semana', blank=True, default=None, null=True)
    category = models.ForeignKey(Categoria, blank=True, null=True, on_delete=models.CASCADE)

    def toJson(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Informe'
        verbose_name_plural = 'Informes'
        db_table = 'informe'
        ordering = ['id']

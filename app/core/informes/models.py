from django.db import models


# Create your models here.
from django.forms import model_to_dict

from core.categorias.models import Categoria
from core.presupuesto.models import Presupuesto
from core.gastos.models import Gastos

class informes(models.Model):
    gastos_id = models.ForeignKey(Gastos, blank=True, null=True, on_delete=models.CASCADE)
    gastos = models.FloatField('Gasto', blank=True, default=None, null=True)
    presupuesto_id = models.ForeignKey(Presupuesto, blank=True, null=True, on_delete=models.CASCADE)
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


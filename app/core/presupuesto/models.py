from datetime import datetime

from django.db import models

# Create your models here.
from django.forms import model_to_dict


class Presupuesto(models.Model):
    date = models.DateField(auto_now=True, verbose_name='Fecha de registro')
    amount = models.DecimalField(max_digits=9, decimal_places=3, verbose_name='Monto')
    category = models.CharField(max_length=50, verbose_name='Categoria')

    def __str__(self):
        return self.date

    def toJson(self):
        item = model_to_dict(self)

        return item

    class Meta:
        verbose_name = 'Presupuesto'
        verbose_name_plural = 'Presupuestos'
        db_table = 'presupuesto'
        ordering = ['id']
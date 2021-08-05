from datetime import datetime

from django.db import models

# Create your models here.

class Presupuesto(models.Model):
    date = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    amount = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Monto')
    category = models.CharField(max_length=50, verbose_name='Categoria')

    def __str__(self):
        return self.date
    class Meta:
        verbose_name = 'Presupuesto'
        verbose_name_plural = 'Presupuestos'
        db_table = 'presupuesto'
        ordering = ['id']
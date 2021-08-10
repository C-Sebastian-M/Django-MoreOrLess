from datetime import datetime
from django.db import models

# Create your models here.

class Gastos(models.Model):
    date = models.DateField(auto_now=True, verbose_name='Fecha de registro')
    amount = models.DecimalField(decimal_places=0, max_digits=15,verbose_name='Monto')
    category = models.CharField(max_length=50, verbose_name='Categoria')

    def __str__(self):
        return self.date
    class Meta:
        verbose_name = 'Gastos'
        verbose_name_plural = 'Gastos'
        db_table = 'gastos'
        ordering = ['id']
from datetime import datetime

from django.db import models

# Create your models here.
from django.forms import model_to_dict


class Categoria(models.Model):
    category = models.CharField(max_length=50, verbose_name='Categoria')

    def __str__(self):
        return self.category

    def toJson(self):
        item = model_to_dict(self)

        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        db_table = 'categoria'
        ordering = ['id']

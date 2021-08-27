from django.db import models
from django.forms import model_to_dict


# Create your models here.

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

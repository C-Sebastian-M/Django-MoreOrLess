from django.db import models
from crum import get_current_user
from django.forms import model_to_dict
from core.models import BaseModel
from core.categorias.models import Categoria


# Create your models here.

# Modelo de la base de datos, obteniendo información del BaseModel, creado para la auditoria de los usuarios
class Gastos(BaseModel):
    date = models.DateField(auto_now=True, verbose_name='Fecha de registro')
    amount = models.FloatField('Monto', blank=True, default=None, null=True)
    category = models.ForeignKey(Categoria, blank=True, null=True, on_delete=models.CASCADE)

    # Metodo de guardado de información
    def save(self, force_insert=False, force_update=False, usig=None,
             update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            self.modified_by = user

        super(Gastos, self).save()

    # Metodo para que la información se guarde en un diccionario
    def toJson(self):
        item = model_to_dict(self)

        return item

    class Meta:
        verbose_name = 'Gasto'
        verbose_name_plural = 'Gastos'
        db_table = 'gastos'
        ordering = ['id']

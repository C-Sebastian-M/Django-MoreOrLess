from crum import get_current_user
from django.db import models
from django.forms import model_to_dict
from core.categorias.models import Categoria
from core.models import BaseModel
from core.presupuesto.models import Presupuesto
from core.gastos.models import Gastos


# Create your models here.

# Modelo de la base de datos, obteniendo información del BaseModel, creado para la auditoria de los usuarios
class informes(BaseModel):
    gastos_id = models.ForeignKey(Gastos, blank=True, null=True, on_delete=models.CASCADE)
    gastos = models.FloatField('Gasto', blank=True, default=None, null=True)
    presupuesto_id = models.ForeignKey(Presupuesto, blank=True, null=True, on_delete=models.CASCADE)
    presupuesto = models.FloatField('presupuesto', blank=True, default=None, null=True)
    date = models.DateField(auto_now=True, verbose_name='Fecha de registro')
    semana = models.FloatField('semana', blank=True, default=None, null=True)
    category = models.ForeignKey(Categoria, blank=True, null=True, on_delete=models.CASCADE)

    # Metodo de guardado de información
    def save(self, force_insert=False, force_update=False, usig=None,
             update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            self.modified_by = user

        super(informes, self).save()

    # Metodo para que la información se guarde en un diccionario
    def toJson(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Informe'
        verbose_name_plural = 'Informes'
        db_table = 'informe'

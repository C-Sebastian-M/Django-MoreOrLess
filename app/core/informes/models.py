from django.db import models
from django.forms import model_to_dict
from core.categorias.models import Categoria
from core.models import BaseModel
from core.presupuesto.models import Presupuesto
from core.gastos.models import Gastos

# Create your models here.


class informes(BaseModel):
    gastos_id = models.ForeignKey(Gastos, blank=True, null=True, on_delete=models.CASCADE)
    gastos = models.FloatField('Gasto', blank=True, default=None, null=True)
    presupuesto_id = models.ForeignKey(Presupuesto, blank=True, null=True, on_delete=models.CASCADE)
    presupuesto = models.FloatField('presupuesto', blank=True, default=None, null=True)
    date = models.DateField(auto_now=True, verbose_name='Fecha de registro')
    semana = models.FloatField('semana', blank=True, default=None, null=True)
    category = models.ForeignKey(Categoria, blank=True, null=True, on_delete=models.CASCADE)

    """def save(self, force_insert=False, force_update=False, usig=None,
                 update_fields=None):
            user = get_current_user()
            if user is not None:
                if not self.pk:
                    self.user_creation = user
                self.modified_by = user

            super(Categoria, self).save()"""

    def toJson(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Informe'
        verbose_name_plural = 'Informes'
        db_table = 'informe'


from datetime import datetime
from crum import get_current_user
from django.db import models
from core.categorias.models import Categoria
from core.models import BaseModel

# Create your models here.


#Modelo de la base de datos, obteniendo información del BaseModel, creado para la auditoria de los usuarios
class Metas(BaseModel):
    f_c_m = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    amount = models.FloatField('Monto', blank=True, default=None, null=True)
    category = models.ForeignKey(Categoria, blank=True, null=True, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True, verbose_name='Fecha de inicio')

    #Metodo de guardado de información
    def save(self, force_insert=False, force_update=False, usig=None,
             update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            self.modified_by = user

        super(Metas, self).save()

    class Meta:
        verbose_name = 'Meta'
        verbose_name_plural = 'Metas'
        db_table = 'meta'
        ordering = ['id']

#Modelo de la base de datos, obteniendo información del BaseModel, creado para la auditoria de los usuarios
class AmountMetas(BaseModel):
    amount = models.FloatField('Monto', blank=True, default=None, null=True)
    #Asociación del modelo Metas con AmountMetas
    meta = models.ForeignKey(Metas, blank=True, null=True, on_delete=models.CASCADE)

    # Metodo de guardado de información
    def save(self, force_insert=False, force_update=False, usig=None,
             update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            self.modified_by = user

        super(AmountMetas, self).save()

    class Meta:
        verbose_name = 'AmountMeta'
        verbose_name_plural = 'AmountMetas'
        db_table = 'AmountMeta'
        ordering = ['id']
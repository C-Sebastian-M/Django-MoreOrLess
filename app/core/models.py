from django.db import models
from django.conf import settings

#Modelo de la base de datos para conseguir la auditoria de los usuarios
class BaseModel(models.Model):
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                                      default=None)
    date_updated = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        abstract = True

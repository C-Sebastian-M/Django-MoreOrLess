from django.contrib import admin
from core.metas.models import Metas

# Register your models here.

# Agregamos nuestro modelo al administrador
admin.site.register(Metas)

from django.contrib import admin
from core.categorias.models import Categoria

# Register your models here.

#Agregamos nuestro modelo al administrador
admin.site.register(Categoria)
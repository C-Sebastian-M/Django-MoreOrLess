from django.contrib import admin
from core.registro.models import RegistroUsuario

# Register your models here.

#Agregamos nuestro modelo al administrador
admin.site.register(RegistroUsuario)
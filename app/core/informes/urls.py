from django.urls import path

from core.informes.views import *

# Urls de las vistas de la aplicación.
urlpatterns = [
    # Vista del listado de la aplicación Gastos.
    path('informes/', InformesListView.as_view(), name='informes'),
]

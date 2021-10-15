from django.urls import path

from core.presupuesto.views import *

# Urls de las vistas de la aplicación.
urlpatterns = [
    # Vista del listado de la aplicación Presupuesto
    path('presupuesto/', PresupuestoListView.as_view(), name='presupuesto'),
    # Vista del formulario de la creación de los Presupuesto
    path('presupuesto/add/', PresupuestoCreateView.as_view(), name='addPre'),
    # Vista del formulario de actualizacion de datos de los Presupuesto
    path('presupuesto/edit/<int:pk>/', PresupuestoUpdateView.as_view(), name='editPre'),
    # Vista del formulario de la eliminacion de datos.
    path('presupuesto/delete/<int:pk>/', PresupuestoDeleteView.as_view(), name='deletePre'),
]

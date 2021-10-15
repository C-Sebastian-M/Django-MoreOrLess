from django.urls import path
from core.gastos.views import GastosListView, GastosCreateView, GastosUpdateView, GastosDeleteView

# Urls de las vistas de la aplicación.
urlpatterns = [
    # Vista del listado de la aplicación Gastos.
    path('gastos/', GastosListView.as_view(), name='gastos'),
    # Vista del formulario de la creación de los Gastos.
    path('gastos/add/', GastosCreateView.as_view(), name='add'),
    # Vista del formulario de actualizacion de datos de los Gastos.
    path('gastos/edit/<int:pk>/', GastosUpdateView.as_view(), name='editGast'),
    # Vista del formulario de la eliminacion de datos.
    path('gastos/delete/<int:pk>/', GastosDeleteView.as_view(), name='deleteGast'),
]
from django.urls import path
from core.gastos.views import GastosListView, GastosCreateView, GastosUpdateView, GastosDeleteView

urlpatterns = [
    path('gastos/', GastosListView.as_view(), name='gastos'),
    path('gastos/add/', GastosCreateView.as_view(), name='add'),
    path('gastos/edit/<int:pk>/', GastosUpdateView.as_view(), name='editGast'),
    path('gastos/delete/<int:pk>/', GastosDeleteView.as_view(), name='deleteGast'),
]
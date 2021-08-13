from django.urls import path
from core.gastos.views import GastosListView, GastosCreateView, GastosUpdateView

urlpatterns = [
    path('gastos/', GastosListView.as_view(), name='gastos'),
    path('gastos/add/', GastosCreateView.as_view(), name='add'),
    path('gastos/edit/<int:pk>/', GastosUpdateView.as_view(), name='editGast'),
]
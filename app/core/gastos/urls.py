from django.urls import path
from core.gastos.views import GastosListView, GastosCreateView

urlpatterns = [
    path('gastos/', GastosListView.as_view(), name='gastos'),
    path('gastos/form/', GastosCreateView.as_view(), name='add')
]
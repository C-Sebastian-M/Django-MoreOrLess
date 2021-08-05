from django.urls import path
from core.gastos.views import GastosListView


urlpatterns = [
    path('gastos/', GastosListView.as_view(), name='gastos'),
]
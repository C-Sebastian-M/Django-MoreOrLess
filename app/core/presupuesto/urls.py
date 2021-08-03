from django.contrib import admin
from django.urls import path

from core.presupuesto.views import PresupuestoListView

urlpatterns = [
    path('', PresupuestoListView.as_view(), name='presupuesto'),
]
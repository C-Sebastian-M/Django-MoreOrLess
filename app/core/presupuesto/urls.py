from django.urls import path

from core.presupuesto.views import *

urlpatterns = [
    path('presupuesto/', PresupuestoListView.as_view(), name='presupuesto'),
    path('presupuesto/add/', PresupuestoCreateView.as_view(), name='addPre'),
    path('presupuesto/edit/<int:pk>/', PresupuestoUpdateView.as_view(), name='editPre'),
    path('presupuesto/delete/<int:pk>/', PresupuestoDeleteView.as_view(), name='deletePre'),
]

from django.urls import path

from core.views import inicio, presupuesto

urlpatterns = [
    path('', inicio),
    path('presupuesto', presupuesto)
]
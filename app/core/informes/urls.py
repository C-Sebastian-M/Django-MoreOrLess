from django.urls import path

from core.informes.views import *

urlpatterns = [
    path('informes/', InformesListView.as_view(), name='informes'),
    path('informes_mensuales/', InformesListView.as_view(), name='informes_mensuales'),
]

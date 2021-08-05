from django.urls import path

from core.perfil.views import *

urlpatterns = [
    path('perfil/', PerfilListView.as_view(), name='perfil'),
]
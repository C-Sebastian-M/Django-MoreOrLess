from django.urls import path
from core.perfil.views import PerfilListView

urlpatterns = [
    path('perfil/', PerfilListView.as_view(), name='perfil'),
]
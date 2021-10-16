from django.urls import path
from core.perfil.views import PerfilListView

#Urls enviadas para las vistas
urlpatterns = [
    #Url donde está el perfil
    path('perfil/', PerfilListView.as_view(), name='perfil'),
]
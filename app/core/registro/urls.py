from django.urls import path
from core.registro.views import RegistroCreateView, UsuarioUpdateView, UsuarioDeleteView

#Urls enviadas para las vistas
urlpatterns = [
    #Url de la vista de creación de información
    path('registro/', RegistroCreateView.as_view(), name='registro'),
    #Url para la vista de actualización de información
    path('usuario/update/', UsuarioUpdateView.as_view(), name='usuarioUpdate'),
    #Url para la eliminación de información
    path('usuario/delete/', UsuarioDeleteView.as_view(), name='usuarioDelete'),

]

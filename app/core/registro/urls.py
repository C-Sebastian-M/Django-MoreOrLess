from django.urls import path
from core.registro.views import RegistroCreateView, UsuarioUpdateView, UsuarioDeleteView

urlpatterns = [
    path('registro/', RegistroCreateView.as_view(), name='registro'),
    path('usuario/update/', UsuarioUpdateView.as_view(), name='usuarioUpdate'),
    path('usuario/delete/', UsuarioDeleteView.as_view(), name='usuarioDelete'),

]

from django.contrib.auth.views import LogoutView
from django.urls import path

from core.login.views import *
#Urls de las vistas de login
urlpatterns = [
    #Vista del logeo del usuario
    path('login/', LoginFormView.as_view(), name='login'),
    #Vista del logout o salida del usuario del sistema
    path('logout/', LogoutView.as_view(), name='logout'),
    #Vista del reseteo de contraseña
    path('reset/password/', ResetPasswordView.as_view(), name='reset'),
    #Vista del cambio de contraseña, enviamos el token para que sea solo para ese usuario
    path('change/password/<str:token>/', ChangePasswordView.as_view(), name='change'),
]

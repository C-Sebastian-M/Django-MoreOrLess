from django.urls import path

from core.views import inicio

urlpatterns = [
    path('', inicio),
]
from django.urls import path

from app.core.views import inicio

urlpatterns = [
    path('uno/', inicio),
    path('dos/', inicio)
]
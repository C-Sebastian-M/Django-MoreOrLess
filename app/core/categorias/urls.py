from django.urls import path

from core.categorias.views import CategoriaCreateView
from core.presupuesto.views import *

urlpatterns = [
    path('categoria/form/', CategoriaCreateView.as_view(), name='addCat'),
]
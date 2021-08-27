from django.urls import path
from core.categorias.views import *

urlpatterns = [
    path('categoria/form/categorias/', CategoriaListView.as_view(), name='categorias'),
    path('categoria/add/', CategoriaCreateView.as_view(), name='addCat'),
    path('categoria/edit/<int:pk>/', CategoriaUpdateView.as_view(), name='editCat'),
    path('categoria/delete/<int:pk>/', CategoriaDeleteView.as_view(), name='deleteCat'),
]

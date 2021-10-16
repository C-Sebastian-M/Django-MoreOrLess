from django.urls import path
from core.categorias.views import *

#Urls dependiendo de la vista
urlpatterns = [
    # Url para la vista de la tabla
    path('categoria/form/categorias/', CategoriaListView.as_view(), name='categorias'),
    #Url de la vista de creación de información
    path('categoria/add/', CategoriaCreateView.as_view(), name='addCat'),
    # Url para la vista de actualización de información
    path('categoria/edit/<int:pk>/', CategoriaUpdateView.as_view(), name='editCat'),
    # Url para la eliminación de información
    path('categoria/delete/<int:pk>/', CategoriaDeleteView.as_view(), name='deleteCat'),
]

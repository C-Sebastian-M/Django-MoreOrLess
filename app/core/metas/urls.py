from django.urls import path
from core.metas.views import MetasListView, MetasCreateView, MetasUpdateView, MetasDeleteView, AmountMetaCreateView

# Urls de las vistas de la aplicación.
urlpatterns = [
    # Vista del listado de la aplicación Metas
    path('metas/', MetasListView.as_view(), name='metas'),
    # Vista del formulario de la creación de las Metas
    path('metas/form/', MetasCreateView.as_view(), name='addMe'),
    # Vista del formulario de creacion del monto de las metas
    path('meta/form/<int:pk>/', AmountMetaCreateView.as_view(), name='addMeAmount'),
    # Vista del formulario de actualizacion de datos de las metas
    path('metas/edit/<int:pk>/', MetasUpdateView.as_view(), name='editMe'),
    # Vista del formulario de la eliminacion de datos.
    path('metas/delete/<int:pk>/', MetasDeleteView.as_view(), name='deleteMe'),
]

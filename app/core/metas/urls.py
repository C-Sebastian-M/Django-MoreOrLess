from django.urls import path
from core.metas.views import MetasListView, MetasCreateView, MetasUpdateView, MetasDeleteView

urlpatterns = [
    path('metas/', MetasListView.as_view(), name='metas'),
    path('metas/form/', MetasCreateView.as_view(), name='addMe'),
    path('metas/edit/<int:pk>/', MetasUpdateView.as_view(), name='editMe'),
    path('metas/delete/<int:pk>/', MetasDeleteView.as_view(), name='deleteMe'),
]

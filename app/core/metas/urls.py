from django.urls import path
from core.metas.views import MetasListView, MetasCreateView

urlpatterns = [
    path('metas/', MetasListView.as_view(), name='metas'),
    path('metas/form/', MetasCreateView.as_view(), name='addMe'),
]
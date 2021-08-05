from django.urls import path
from core.metas.views import MetasListView

urlpatterns = [
    path('metas/', MetasListView.as_view(), name='metas'),
]
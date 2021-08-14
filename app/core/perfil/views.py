from django.shortcuts import render
from django.views.generic import ListView

from core import perfil
from core.perfil.models import user
from core.presupuesto.models import Presupuesto

# Create your views here.


class PerfilListView(ListView):
    model = user
    template_name = 'perfil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['index_url'] = reverse_lazy('index')
        return context
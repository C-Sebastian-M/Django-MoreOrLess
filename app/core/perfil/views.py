from django.shortcuts import render
from django.views.generic import ListView
from core.perfil.models import Perfil

# Create your views here.


class PerfilListView(ListView):
    model = Perfil
    template_name = 'perfil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['index_url'] = reverse_lazy('index')
        return context
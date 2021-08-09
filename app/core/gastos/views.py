from django.shortcuts import render
from django.views.generic import ListView
from core.gastos.models import Gastos

# Create your views here.

class GastosListView(ListView):
    model = Gastos
    template_name = 'gastos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Gastos registrados'
        #context['index_url'] = reverse_lazy('index')
        return context
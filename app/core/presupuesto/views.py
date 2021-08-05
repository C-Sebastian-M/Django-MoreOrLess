from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from core.presupuesto.models import Presupuesto


class PresupuestoListView(ListView):
    model = Presupuesto
    template_name = 'presupuesto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Pesupuestos registrados'
        #context['index_url'] = reverse_lazy('index')
        return context
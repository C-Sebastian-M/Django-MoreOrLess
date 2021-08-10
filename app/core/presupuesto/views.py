from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from core.presupuesto.forms import PresupuestoForm
from core.presupuesto.models import Presupuesto

# Create your views here.

class PresupuestoListView(ListView):
    model = Presupuesto
    template_name = 'presupuesto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Pesupuestos registrados'
        #context['index_url'] = reverse_lazy('index')
        return context

class PresupuestoCreateView(CreateView):
    model = Presupuesto
    form_class = PresupuestoForm
    template_name = 'formularios/form_presupuesto.html'
    success_url = reverse_lazy('presupuesto')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ingresar presupuesto'
        return context
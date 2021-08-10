from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from core.gastos.forms import GastosForm
from core.gastos.models import Gastos


# Create your views here.

class GastosListView(ListView):
    model = Gastos
    template_name = 'gastos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Gastos registrados'
        return context


class GastosCreateView(CreateView):
    model = Gastos
    form_class = GastosForm
    template_name = 'formularios/form_gastos.html'
    success_url = reverse_lazy('gastos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ingresar gastos'
        return context

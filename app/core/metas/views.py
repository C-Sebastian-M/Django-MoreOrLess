from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from core.metas.forms import MetasForm
from core.metas.models import Metas


# Create your views here.
class MetasListView(ListView):
    model = Metas
    template_name = 'metas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MetasCreateView(CreateView):
    model = Metas
    form_class = MetasForm
    template_name = 'formularios/form_metas.html'
    success_url = reverse_lazy('metas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ingresar meta'
        return context

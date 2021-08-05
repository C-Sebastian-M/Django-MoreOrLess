from django.shortcuts import render
from django.views.generic import ListView
from core.presupuesto.models import Presupuesto

# Create your views here.


class InformesListView(ListView):
    model = Presupuesto
    template_name = 'informes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['index_url'] = reverse_lazy('index')
        return context
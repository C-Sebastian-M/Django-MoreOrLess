from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from core.metas.models import Metas


class MetasListView(ListView):
    model = Metas
    template_name = 'metas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['index_url'] = reverse_lazy('index')
        return context
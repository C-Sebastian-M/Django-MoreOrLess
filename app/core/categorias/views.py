from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic import CreateView

from core.categorias.forms import CategoriaForm
from core.categorias.models import Categoria


# Create your views here.


class CategoriaCreateView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'formularios/form_categoria.html'
    success_url = reverse_lazy('')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar categoria'
        return context

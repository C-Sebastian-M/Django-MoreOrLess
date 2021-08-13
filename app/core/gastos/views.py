from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
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

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ingresar gastos'
        return context

class GastosUpdateView(UpdateView):
    model = Gastos
    form_class = GastosForm
    template_name = 'formularios/form_gastos.html'
    success_url = reverse_lazy('gastos')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar gastos'
        context['action'] = 'edit'

        return context


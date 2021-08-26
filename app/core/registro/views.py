from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from core.registro.forms import RegistroForm
from core.registro.models import Registro

# Create your views here.

class RegistroCreateView(CreateView):
    model = Registro
    form_class = RegistroForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrarse'
        context['list_url'] = reverse_lazy('login')
        context['action'] = 'add'
        return context
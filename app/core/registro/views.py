from core.registro.forms import RegistroUsuariosForm
from core.registro.models import RegistroUsuario
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

# Create your views here.



class RegistroCreateView(CreateView):
    model = RegistroUsuario
    form_class = RegistroUsuariosForm
    template_name = 'registro.html'
    success_url = reverse_lazy('index')

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
        context['title'] = 'Registro de usuario'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('index')
        return context
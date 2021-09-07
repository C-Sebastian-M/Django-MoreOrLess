from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from core.registro.forms import RegistroUsuariosForm
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from core.registro.models import RegistroUsuario


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

class UsuarioUpdateView(UpdateView):
    model = RegistroUsuario
    form_class = RegistroUsuariosForm
    template_name = 'form_usuario.html'
    success_url = reverse_lazy('perfil')

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

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
        context['title'] = 'Editar usuario'
        context['list_url'] = reverse_lazy('perfil')
        context['action'] = 'edit'
        return context

class UsuarioDeleteView(DeleteView):
    model = RegistroUsuario
    template_name = 'delete_usuario.html'
    success_url = reverse_lazy('login')

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar usuario'
        context['list_url'] = reverse_lazy('login')
        return context
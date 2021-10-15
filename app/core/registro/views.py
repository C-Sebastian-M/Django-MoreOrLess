from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from core.registro.forms import RegistroUsuariosForm
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from core.registro.models import RegistroUsuario


# Create your views here.

# Vista de formulario para crear información en la base de datos de los usuarios.
class RegistroCreateView(CreateView):
    #Especificación del modelo donde se guardara la información
    model = RegistroUsuario
    #La clase de formulario que vamos a utilizar para mostrar los campos de ingreso de información.
    form_class = RegistroUsuariosForm
    #Especificación del template html que vamos a utilizar
    template_name = 'registro.html'
    #Url a la que se retornará despues de diligenciar el formulario.
    success_url = reverse_lazy('index')

    #Metodo post para guardar la información en la base de datos.
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

#Vista de formulario para actualizar los datos de los usuarios
class UsuarioUpdateView(UpdateView):
    # Especificación del modelo donde se actualizara la información
    model = RegistroUsuario
    # La clase de formulario que vamos a utilizar para mostrar los campos de ingreso de información.
    form_class = RegistroUsuariosForm
    # Especificación del template html que vamos a utilizar
    template_name = 'form_usuario.html'
    # Url a la que se retornará despues de diligenciar el formulario.
    success_url = reverse_lazy('perfil')

    # Metodo de seguridad
    @method_decorator(csrf_exempt)
    # Metodo para requerir estar logeado
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    # Metodo post para guardar la información en la base de datos.
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

#Vista para borrar información de los usuarios en la base de datos
class UsuarioDeleteView(DeleteView):
    # Especificación del modelo donde se eliminará la información
    model = RegistroUsuario
    # Especificación del template html que vamos a utilizar
    template_name = 'delete_usuario.html'
    # Url a la que se retornará despues de diligenciar el formulario.
    success_url = reverse_lazy('login')

    #Metodo de seguridad
    @method_decorator(csrf_exempt)
    #Metodo para requerir estar logeado
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    # Metodo post para guardar la información en la base de datos.
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
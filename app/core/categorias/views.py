#Traemos diferentes funciones que nos da django y nuestras funciones para el funcionamiento de los elementos
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from core.categorias.forms import CategoriaForm
from core.categorias.models import Categoria

#Aquí van a estar la listview, que es una tabla con datos
class CategoriaListView(ListView):
    # Especificación del modelo donde se actualizara la información
    model = Categoria
    # Especificación del template html que vamos a utilizar
    template_name = 'categorias.html'

    #Función de discriminación de usuarios
    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(user_creation_id=user)

    #decorador de registro obligatorio
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Categorias creadas'
        return context

# Vista de formulario para crear información en la base de datos de las catgorias.
class CategoriaCreateView(CreateView):
    # Especificación del modelo donde se guardara la información
    model = Categoria
    # La clase de formulario que vamos a utilizar para mostrar los campos de ingreso de información.
    form_class = CategoriaForm
    # Especificación del template html que vamos a utilizar
    template_name = 'form_categoria.html'
    # Url a la que se retornará despues de diligenciar el formulario.
    success_url = reverse_lazy('')

    # Metodo de seguridad
    @method_decorator(csrf_exempt)
    # Metodo para requerir estar logeado
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = None
        return super().dispatch(request, *args, **kwargs)

    # Metodo post para guardar la información en la base de datos.
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
        context['title'] = 'Registrar categoria'
        context['list_url'] = reverse_lazy('categorias')
        context['action'] = 'add'
        return context

#Vista de formulario para actualizar la categoria
class CategoriaUpdateView(UpdateView):
    # Especificación del modelo donde se actualizara la información
    model = Categoria
    # La clase de formulario que vamos a utilizar para mostrar los campos de ingreso de información.
    form_class = CategoriaForm
    # Especificación del template html que vamos a utilizar
    template_name = 'form_categoria.html'
    # Url a la que se retornará despues de diligenciar el formulario.
    success_url = reverse_lazy('')

    #Metodo de seguridad
    @method_decorator(csrf_exempt)
    # Metodo para requerir estar logeado
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

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
        context['title'] = 'Editar categoria'
        context['list_url'] = reverse_lazy('categorias')
        context['action'] = 'edit'

        return context

#Vista para borrar información de las categorias en la base de datos
class CategoriaDeleteView(DeleteView):
    # Especificación del modelo donde se eliminará la información
    model = Categoria
    # Especificación del template html que vamos a utilizar
    template_name = 'delete_categoria.html'
    # Url a la que se retornará despues de diligenciar el formulario.
    success_url = reverse_lazy('categorias')

    # Metodo de seguridad
    @method_decorator(csrf_exempt)
    # Metodo para requerir estar logeado
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

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
        context['title'] = 'Eliminar categoria'
        context['list_url'] = reverse_lazy('categorias')
        return context
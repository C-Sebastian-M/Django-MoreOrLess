from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.metas.forms import MetasForm, MetaForm
from core.metas.models import Metas, AmountMetas
from core.categorias.models import Categoria
from django.db.models import FloatField, Sum
from crum import get_current_user


# Create your views here.

# Vista de la lista de la aplicación metas
class MetasListView(ListView):
    # Modelo del que vamos a conseguir la información para plasmarlo en la tabla
    model = Metas
    # La plantilla html que utilizaremos para el front end
    template_name = 'metas.html'

    # Obtenemos el usuario por medio de get_query
    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(user_creation_id=user)

    # Metodo de seguridad
    @method_decorator(csrf_exempt)
    # Metodo de requerimiento de logeo para mostrar la información
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # Ahorro sugerido por dia
    def ahorro_dia(self):
        # Variable usuario para poder aplicar auditoria en la aplicación
        user = self.request.user
        # Filtramos por el usuario y agregamos la suma de los montos de las metas de la base de datos
        valores_dia = Metas.objects.filter(user_creation_id=user).aggregate(total_meta=Sum('amount'))
        # Buscamos esos valores
        valores_dia = valores_dia['total_meta']
        # Hacemos una validación para mostrar la información en nuestra pagina
        if valores_dia is None:
            valores_dia = 0
            return valores_dia
        else:
            # Operación para conseguir el valor por dia
            tot = valores_dia / 31
            return tot

    # Ahorro sugerido de manera mensual
    def ahorro_men(self):
        # Variable usuario para poder aplicar auditoria en la aplicación
        user = self.request.user
        # Filtramos por usuario y agregamos la suma del monto de las metas de la base de datos
        valores = Metas.objects.filter(user_creation_id=user).aggregate(total_meta=Sum('amount'))
        # Obtenemos ese valor sobreescribiendo la variable
        valores = valores['total_meta']
        # Validación para mostrar la información en nuestro aplicativo
        if valores is None:
            valores = 0
            return valores
        else:
            # Operación matematica para obtener el ahorro mensual por un año
            tot = valores / 12
            return tot

    # Porcentaje para las metas
    def metas(self):
        # Variable usuario para poder aplicar auditoria en la aplicación
        user = self.request.user
        # Filtramos por el usuario
        valores_metas = Metas.objects.filter(user_creation_id=user)
        # Obtenemos los datos de la base de datos por sus id
        Catego = Metas.objects.all().values_list('id', flat=True)
        # Creamos un array donde quedara la información
        porcentaje = []
        # Ciclo for para encontrar información de solo la meta que se va a mostrar
        for c in Catego:
            # Variable para filtrar por usuario y por el id de la meta
            variable = AmountMetas.objects.filter(user_creation_id=user, meta_id=c)
            # Inicializamos una variable total que recogera valores en el siguiente ciclo
            total = 0
            # Ciclo para buscar información en AmountMetas
            for v in variable:
                # Validacion para ver si si existe un monto registrado
                if v is None:
                    continue
                else:
                    # Si existe el total se incrementa por el monto que el usuario registre
                    total += v.amount
            # Se agrega al array la información del total
            porcentaje.append(total)

        # Se inicializan los datos de la base de dato de Metas, como arrays
        id, gastos, category_id, f_c_m, date = [], [], [], [], []

        # Ciclo for, para agregar información a las arrays dependiendo del usuario, ya que lo hemos filtrado en valores_meta
        for v in valores_metas:
            id.append(v.id)
            gastos.append(v.amount)
            obj = Categoria.objects.get(pk=v.category_id)
            category_id.append(obj)
            f_c_m.append(v.f_c_m)
            date.append(v.date)

        # Inicializamos la variable barra como una array
        barra = []
        # Ciclo for para agregar información a la barra
        for i in range(len(gastos)):
            barra.append(int(porcentaje[i] * 100 / gastos[i]))
        print(barra)

        metas = zip(id, gastos, category_id, f_c_m, date, barra)
        return metas

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['metas'] = self.metas()
        context['ahorro_dia'] = self.ahorro_dia()
        context['ahorro_men'] = self.ahorro_men()
        return context


# Vista del formulario para ingresar información a la base de datos
class MetasCreateView(CreateView):
    # Especificamos el modelo al cual se le agregara la información
    model = Metas
    # Especificamos el formulario
    form_class = MetasForm
    # Plantilla del front end
    template_name = 'form_metas.html'
    # Url de redirección al completar el formulario
    success_url = reverse_lazy('metas')

    def get_form_kwargs(self):
        kwargs = super(MetasCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user.id})
        return kwargs

    # Obtenemos la información del usuario, filtrando por el mismo
    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(user_creation_id=user)

    # Metodo de seguridad
    @method_decorator(csrf_exempt)
    # Metodo de requerimiento de logeo
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = None
        return super().dispatch(request, *args, **kwargs)

    # Metodo post para guardar la información del formulario
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
        context['title'] = 'Ingresar meta'
        context['list_url'] = reverse_lazy('metas')
        context['action'] = 'add'
        return context


# Vista del formulario para actualizar información de la base de datos
class MetasUpdateView(UpdateView):
    # Especificamos el modelo al cual se le actualizara la información
    model = Metas
    # Especificamos el formulario
    form_class = MetasForm
    # Plantilla del front end
    template_name = 'form_metas.html'
    # Url de redirección al completar el formulario
    success_url = reverse_lazy('metas')

    # Metodo de seguridad
    @method_decorator(csrf_exempt)
    # Metodo de requerimiento de logeo
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    # Metodo post de guardado de información
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
        context['list_url'] = reverse_lazy('metas')
        context['action'] = 'edit'

        return context


# Vista del formulario para eliminar información de la base de datos
class MetasDeleteView(DeleteView):
    # Especificamos el modelo al cual se le eliminara la información
    model = Metas
    #  Plantilla del front end
    template_name = 'delete_metas.html'
    # Url de redirección al autorizar la acción
    success_url = reverse_lazy('metas')

    # Metodo de seguridad
    @method_decorator(csrf_exempt)
    # Metodo de requerimiento de logeo
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    # Metodo post de borrado de la informacion
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar meta'
        context['list_url'] = reverse_lazy('metas')
        return context


# Vista del formulario de Amount, para ingresar información del progreso de las metas
class AmountMetaCreateView(CreateView):
    # Especificamos el modelo al cual se le ingresara la información
    model = AmountMetas
    # Especificamos el formulario
    form_class = MetaForm
    # Plantilla html del front end
    template_name = 'form_metas.html'
    # Url de redirección al completar el formulario
    success_url = reverse_lazy('metas')

    # Metodo de seguridad
    @method_decorator(csrf_exempt)
    # Metodo de requerimiento del logeo
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = None
        return super().dispatch(request, *args, **kwargs)

    # Metodo post para guardar la información
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = MetaForm(request.POST)
                if form.is_valid():
                    form.instance.meta_id = self.kwargs['pk']
                    form.instance.save()
            else:
                data['error'] = 'No ha ingresado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ingresar dinero a la meta'
        context['list_url'] = reverse_lazy('metas')
        context['action'] = 'add'
        return context

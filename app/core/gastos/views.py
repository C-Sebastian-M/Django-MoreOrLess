from datetime import datetime
from datetime import timedelta
import calendar

from django.contrib.auth.decorators import login_required
from django.db.models import FloatField, Sum
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.gastos.forms import GastosForm
from core.gastos.models import Gastos
# Create your views here.
from core.informes.models import informes


# Metodo que funciona como un calendario y enumera las semanas del mes.
def week(dt):
    mth = calendar.monthcalendar(dt.year, dt.month)
    for i, wk in enumerate(mth):
        if dt.day in wk:
            return i + 1


# Vista de la lista de la aplicación gastos.
class GastosListView(ListView):
    # Modelo del que vamos a conseguir la información para plasmarlo en la tabla.
    model = Gastos
    # La plantilla html que utilizaremos para el front end.
    template_name = 'gastos.html'

    # Obtenemos el usuario por medio de get_query.
    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(user_creation_id=user)

    # Metodo de seguridad
    @method_decorator(csrf_exempt)
    # Metodo de requerimiento de logeo para mostrar la información
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # Metodo post para enviar la información de la grafica.
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'obtener_reporte_gastos_sem':
                data = self.obtener_reporte_gastos_sem()
            else:
                data['error'] = 'Ha ocurrido un error '
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    # Metodo para obtener la información de la grafica a traves de filtros y el calendario que se gardara en una lista.
    def obtener_reporte_gastos_sem(self):
        year = datetime.now().year
        month = datetime.now().month
        user = self.request.user
        date = datetime.now().today()
        start_week = date - timedelta(date.weekday())
        end_week = start_week + timedelta(7)
        data = []
        # Ciclo para filtrar la informacion por dia de la semana.
        for w in range(1, 8):
            dict_data = Gastos.objects.filter(user_creation=user, date__year=year, date__month=month,
                                              date__range=[start_week, end_week], date__week_day=w).aggregate(
                Sum('amount', output_field=FloatField()))
            if dict_data['amount__sum'] is None:
                data.append(0)
            else:
                data.append(float(dict_data['amount__sum']))
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reporte_gastos_sem'] = self.obtener_reporte_gastos_sem()
        context['title'] = 'Gastos registrados'
        return context


# Vista del formulario para ingresar información a la base de datos
class GastosCreateView(CreateView):
    # Especificamos el modelo al cual se le agregara la información
    model = Gastos
    # Especificamos el formulario
    form_class = GastosForm
    # Plantilla del front end
    template_name = 'form_gastos.html'
    # Url de redirección al completar el formulario
    success_url = reverse_lazy('gastos')

    # Enviar objeto de usuario al formulario, para verificar qué campos mostrar / eliminar (según el grupo)
    def get_form_kwargs(self):
        kwargs = super(GastosCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user.id})
        return kwargs

    # Obtenemos la información del usuario, filtrando por el mismo
    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(user_creation_id=user)

    # Metodo de requerimiento de logeo
    @method_decorator(login_required)
    # Metodo de seguridad
    @method_decorator(csrf_exempt)
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
        context['title'] = 'Ingresar gastos'
        context['list_url'] = reverse_lazy('gastos')
        context['action'] = 'add'
        return context


# Vista del formulario para actualizar información de la base de datos
class GastosUpdateView(UpdateView):
    # Especificamos el modelo al cual se le actualizara la información
    model = Gastos
    # Especificamos el formulario
    form_class = GastosForm
    # Plantilla del front end
    template_name = 'form_gastos.html'
    # Url de redirección al completar el formulario
    success_url = reverse_lazy('gastos')

    # Metodo de requerimiento de logeo
    @method_decorator(login_required)
    # Metodo de seguridad
    @method_decorator(csrf_exempt)
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
        context['title'] = 'Editar gastos'
        context['list_url'] = reverse_lazy('gastos')
        context['action'] = 'edit'
        return context


# Vista del formulario para eliminar información de la base de datos
class GastosDeleteView(DeleteView):
    # Especificamos el modelo al cual se le eliminara la información
    model = Gastos
    #  Plantilla del front end
    template_name = 'delete_gastos.html'
    # Url de redirección al autorizar la acción
    success_url = reverse_lazy('gastos')

    # Metodo de requerimiento de logeo
    @method_decorator(login_required)
    # Metodo de seguridad
    @method_decorator(csrf_exempt)
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
        context['title'] = 'Eliminar gasto'
        context['list_url'] = reverse_lazy('gastos')
        return context

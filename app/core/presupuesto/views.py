from datetime import datetime
from datetime import timedelta
import calendar
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, FloatField
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.presupuesto.forms import PresupuestoForm
from core.presupuesto.models import Presupuesto

from core.informes.models import informes



# Create your views here.

def week(dt):
    mth = calendar.monthcalendar(dt.year, dt.month)
    for i, wk in enumerate(mth):
        if dt.day in wk:
            return i + 1


class PresupuestoListView(ListView):
    model = Presupuesto
    template_name = 'presupuesto.html'

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(user_creation_id=user)

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'obtener_reporte_presupuesto_sem':
                data = self.obtener_reporte_presupuesto_sem()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def obtener_reporte_presupuesto_sem(self):
        year = datetime.now().year
        month = datetime.now().month
        user = self.request.user
        date = datetime.now().today()
        start_week = date - timedelta(date.weekday())
        end_week = start_week + timedelta(7)
        print([start_week, end_week])
        data = []
        for w in range(1, 8):
            dict_data = Presupuesto.objects.filter(user_creation= user,date__year=year, date__month=month,
                                                   date__range=[start_week, end_week],date__week_day=w).aggregate(
                Sum('amount', output_field=FloatField()))
            if (dict_data['amount__sum'] == None):
                data.append(0)
            else:
                data.append(float(dict_data['amount__sum']))
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reporte_presupesto_sem'] = self.obtener_reporte_presupuesto_sem()
        context['title'] = 'Presupuestos registrados'
        return context


class PresupuestoCreateView(CreateView):
    model = Presupuesto
    form_class = PresupuestoForm
    template_name = 'form_presupuesto.html'
    success_url = reverse_lazy('presupuesto')

    # Sending user object to the form, to verify which fields to display/remove (depending on group)
    def get_form_kwargs(self):
        kwargs = super(PresupuestoCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user.id})
        return kwargs

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(user_creation_id=user)

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = None
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
        context['title'] = 'Ingresar presupuesto'
        context['list_url'] = reverse_lazy('presupuesto')
        context['action'] = 'add'
        return context


class PresupuestoUpdateView(UpdateView):
    model = Presupuesto
    form_class = PresupuestoForm
    template_name = 'form_presupuesto.html'
    success_url = reverse_lazy('presupuesto')

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
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
                data['error'] = 'No ha ingresado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar presupuesto'
        context['list_url'] = reverse_lazy('presupuesto')
        context['action'] = 'edit'
        return context


class PresupuestoDeleteView(DeleteView):
    model = Presupuesto
    template_name = 'delete_presupuesto.html'
    success_url = reverse_lazy('presupuesto')

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar presupuesto'
        context['list_url'] = reverse_lazy('presupuesto')
        return context

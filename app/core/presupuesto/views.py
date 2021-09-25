from datetime import datetime
import calendar

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, FloatField
from django.http import JsonResponse

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.informes.models import informes
from core.presupuesto.forms import PresupuestoForm
from core.presupuesto.models import Presupuesto


# Create your views here.

def week(dt):
    mth = calendar.monthcalendar(dt.year, dt.month)
    for i, wk in enumerate(mth):
        if dt.day in wk:
            return i + 1


class PresupuestoListView(ListView):
    model = Presupuesto
    template_name = 'presupuesto.html'

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
        data = []
        for w in range(1, 8):
            dict_data = Presupuesto.objects.filter(date__year=year, date__month=month,
                                                   date__week_day=w).aggregate(
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

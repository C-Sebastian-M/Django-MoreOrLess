from datetime import datetime
import calendar
import calendar

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


def week(dt):
    mth = calendar.monthcalendar(dt.year, dt.month)
    for i, wk in enumerate(mth):
        if dt.day in wk:
            return i + 1


class GastosListView(ListView):
    model = Gastos
    template_name = 'gastos.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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

    def obtener_reporte_gastos_sem(self):
        year = datetime.now().year
        month = datetime.now().month
        data = []
        for w in range(1, 8):
            dict_data = Gastos.objects.filter(date__year=year, date__month=month, date__week_day=w).aggregate(
                Sum('amount', output_field=FloatField()))
            if (dict_data['amount__sum'] == None):
                data.append(0)
            else:
                data.append(float(dict_data['amount__sum']))
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reporte_gastos_sem'] = self.obtener_reporte_gastos_sem()
        context['title'] = 'Gastos registrados'
        return context


class GastosCreateView(CreateView):
    model = Gastos
    form_class = GastosForm
    template_name = 'form_gastos.html'
    success_url = reverse_lazy('gastos')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
                informe = informes()
                informe.gastos = form.cleaned_data.get('amount')
                informe.category = form.cleaned_data.get('category')
                informe.semana = week(datetime(datetime.now().year, datetime.now().month, datetime.now().day))
                informe.save()
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


class GastosUpdateView(UpdateView):
    model = Gastos
    form_class = GastosForm
    template_name = 'form_gastos.html'
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
        context['list_url'] = reverse_lazy('gastos')
        context['action'] = 'edit'
        return context


class GastosDeleteView(DeleteView):
    model = Gastos
    template_name = 'delete_gastos.html'
    success_url = reverse_lazy('gastos')

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
        context['title'] = 'Eliminar gasto'
        context['list_url'] = reverse_lazy('gastos')
        return context

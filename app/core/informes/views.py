from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import FloatField, Sum
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from core.categorias.models import Categoria
from core.gastos.models import Gastos
from core.gastos.views import week
from core.informes.models import informes


# Create your views here.


class InformesListView(ListView):
    model = informes
    template_name = 'informes.html'

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.porcentaje_gastos_semanales()
        return super().dispatch(request, *args, **kwargs)

    def porcentaje_gastos_semanales(self):
        data = []
        total = 0
        year = datetime.now().year
        month = datetime.now().month
        w = week(datetime(datetime.now().year, datetime.now().month, datetime.now().day))

        try:
            Catego = Categoria.objects.all().values_list('id', flat=True)

            for c in Catego:
                variable = informes.objects.filter(category_id=c, date__year=year, date__month=month,
                                                   semana=w).aggregate(Sum('gastos', output_field=FloatField()))
                name = Categoria.objects.filter(id=c)
                data.append({
                    'name': str(name[0]),
                    'y': variable["gastos__sum"]
                })

            for d in data:
                total += d['y']
        except:
            pass

        return data, total

    def porcentaje_gastos_mensuales(self):
        data = []
        total = 0
        year = datetime.now().year
        month = datetime.now().month

        try:
            Catego = Categoria.objects.all().values_list('id', flat=True)

            for c in Catego:
                variable = informes.objects.filter(category_id=c, date__year=year, date__month=month).aggregate(
                    Sum('gastos', output_field=FloatField()))
                name = Categoria.objects.filter(id=c)
                data.append({
                    'name': str(name[0]),
                    'y': variable["gastos__sum"]
                })

            for d in data:
                total += d['y']
        except:
            pass

        return data, total

    def porcentaje_gastos_anuales(self):
        data = []
        total = 0
        year = datetime.now().year

        try:
            Catego = Categoria.objects.all().values_list('id', flat=True)

            for c in Catego:
                variable = informes.objects.filter(category_id=c, date__year=year).aggregate(
                    Sum('gastos', output_field=FloatField()))
                name = Categoria.objects.filter(id=c)
                data.append({
                    'name': str(name[0]),
                    'y': variable["gastos__sum"]
                })

            for d in data:
                total += d['y']
        except:
            pass
        return data, total

    def porcentaje_presupuestos_semanales(self):
        data = []
        totalP = 0
        year = datetime.now().year
        month = datetime.now().month
        w = week(datetime(datetime.now().year, datetime.now().month, datetime.now().day))

        Catego = Categoria.objects.all().values_list('id', flat=True)

        for c in Catego:
            variable = informes.objects.filter(category_id=c, date__year=year, date__month=month,
                                               semana=w).aggregate(Sum('presupuesto', output_field=FloatField()))
            name = Categoria.objects.filter(id=c)
            data.append({
                'name': str(name[0]),
                'y': variable["presupuesto__sum"]
            })

        for d in data:
            if d['y'] == None:
                pass
            else:
                totalP += d['y']
        return data, totalP

    def porcentaje_presupuestos_mensuales(self):
        data = []
        totalP = 0
        year = datetime.now().year
        month = datetime.now().month

        Catego = Categoria.objects.all().values_list('id', flat=True)

        for c in Catego:
            variable = informes.objects.filter(category_id=c, date__year=year, date__month=month).aggregate(
                Sum('presupuesto', output_field=FloatField()))
            name = Categoria.objects.filter(id=c)
            data.append({
                'name': str(name[0]),
                'y': variable["presupuesto__sum"]
            })

        for d in data:
            if d['y'] == None:
                pass
            else:
                totalP += d['y']
        return data, totalP

    def porcentaje_presupuestos_anuales(self):
        data = []
        totalP = 0
        year = datetime.now().year

        Catego = Categoria.objects.all().values_list('id', flat=True)

        for c in Catego:
            variable = informes.objects.filter(category_id=c, date__year=year).aggregate(
                Sum('presupuesto', output_field=FloatField()))
            name = Categoria.objects.filter(id=c)
            data.append({
                'name': str(name[0]),
                'y': variable["presupuesto__sum"]
            })

        for d in data:
            if d['y'] == None:
                pass
            else:
                totalP += d['y']
        return data, totalP

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'porcentaje_gastos_semanales':
                data_grafico, _ = self.porcentaje_gastos_semanales()
                data = {
                    'name': 'Porcentaje',
                    'colorByPoint': True,
                    'data': data_grafico,
                }
            elif action == 'porcentaje_gastos_mensuales':
                data_graficoM, _ = self.porcentaje_gastos_mensuales()
                data = {
                    'name': 'Porcentaje',
                    'colorByPoint': True,
                    'data': data_graficoM,
                }
            elif action == 'porcentaje_gastos_anuales':
                data_graficoA, _ = self.porcentaje_gastos_anuales()
                data = {
                    'name': 'Porcentaje',
                    'colorByPoint': True,
                    'data': data_graficoA,
                }
            elif action == 'porcentaje_presupuestos_semanales':
                data_graficoPS, _ = self.porcentaje_presupuestos_semanales()
                data = {
                    'name': 'Porcentaje',
                    'colorByPoint': True,
                    'data': data_graficoPS,
                }
            elif action == 'porcentaje_presupuestos_mensuales':
                data_graficoPM, _ = self.porcentaje_presupuestos_mensuales()
                data = {
                    'name': 'Porcentaje',
                    'colorByPoint': True,
                    'data': data_graficoPM,
                }
            elif action == 'porcentaje_presupuestos_anuales':
                data_graficoPA, _ = self.porcentaje_presupuestos_anuales()
                data = {
                    'name': 'Porcentaje',
                    'colorByPoint': True,
                    'data': data_graficoPA,
                }
            else:
                data['error'] = 'Ha ocurrido un error '
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _, total = self.porcentaje_gastos_semanales()
        _, total = self.porcentaje_gastos_mensuales()
        _, total = self.porcentaje_gastos_anuales()
        _, totalP = self.porcentaje_presupuestos_semanales()
        _, totalP = self.porcentaje_presupuestos_mensuales()
        _, totalP = self.porcentaje_presupuestos_anuales()
        # context['index_url'] = reverse_lazy('index')
        context['gastos_t'] = total
        context['presupuesto_t'] = totalP
        context['restante'] = totalP - total
        return context

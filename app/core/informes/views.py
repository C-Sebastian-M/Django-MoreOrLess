from datetime import datetime
import calendar
from crum import get_current_user

from django.contrib.auth.decorators import login_required
from django.db.models import FloatField, Sum
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from core.categorias.models import Categoria
from core.gastos.models import Gastos
from core.presupuesto.models import Presupuesto
from core.informes.models import informes


# Metodo que funciona como un calendario y enumera las semanas del mes.
def week(dt):
    mth = calendar.monthcalendar(dt.year, dt.month)
    for i, wk in enumerate(mth):
        if dt.day in wk:
            return i + 1


# Create your views here.

# Vista de la lista de la aplicación informes.
class InformesListView(ListView):
    # Modelo del que vamos a conseguir la información para plasmarlo en la tabla.
    model = informes
    # La plantilla html que utilizaremos para el front end.
    template_name = 'informes.html'

    # Obtenemos el usuario por medio de get_query.
    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(user_creation_id=user)

    # Metodo de requerimiento de logeo para mostrar la información
    @method_decorator(login_required)
    # Metodo de seguridad
    @method_decorator(csrf_exempt)
    # Metodo dispatch para traer todos los objetos de la base de datos de categorias, gastos y presupuesto.
    def dispatch(self, request, *args, **kwargs):
        informes.objects.all().delete()
        valores_gastos = Gastos.objects.filter(user_creation_id=get_current_user())
        valores_presupesto = Presupuesto.objects.filter(user_creation_id=get_current_user())

        for v in valores_gastos:
            informe = informes()
            informe.gastos = v.amount
            informe.category_id = v.category_id
            informe.gastos_id_id = v.id
            informe.semana = week(datetime(v.date.year, v.date.month, v.date.day))
            # informe.user_creation = get_current_user()
            informe.save()

        for v in valores_presupesto:
            informe = informes()
            informe.presupuesto = v.amount
            informe.category_id = v.category_id
            informe.presupuesto_id_id = v.id
            informe.semana = week(datetime(v.date.year, v.date.month, v.date.day))
            # informe.user_creation = get_current_user()
            informe.save()
        self.porcentaje_gastos_semanales()
        return super().dispatch(request, *args, **kwargs)

    # Metodo para obtener la información de la grafica a traves de filtros y el calendario que se gardara en una lista.
    def porcentaje_gastos_semanales(self):
        data = []
        total = 0
        year = datetime.now().year
        month = datetime.now().month
        w = week(datetime(datetime.now().year, datetime.now().month, datetime.now().day))
        # Validación para traer los id de las categorias creadas por cada usuario.
        try:
            Catego = Categoria.objects.all().values_list('id', flat=True)
            # Ciclo para filtrar la información por las categorias y la semana del mes.
            for c in Catego:
                variable = informes.objects.filter(category_id=c, date__year=year, date__month=month,
                                                   semana=w).aggregate(Sum('gastos', output_field=FloatField()))
                name = Categoria.objects.filter(id=c)
                data.append({
                    'name': str(name[0]),
                    'y': variable["gastos__sum"]
                })
            # Se obtiene el total del monto de los gastos ingresados.
            for d in data:
                total += d['y']
        except:
            pass
        return data, total

    # Metodo para obtener la información de la grafica a traves de filtros y el calendario que se gardara en una lista.
    def porcentaje_gastos_mensuales(self):
        data = []
        total = 0
        year = datetime.now().year
        month = datetime.now().month
        # Validación para traer los id de las categorias creadas por cada usuario.
        try:
            Catego = Categoria.objects.all().values_list('id', flat=True)
            # Ciclo para filtrar la información por las categorias y la meses del año.
            for c in Catego:
                variable = informes.objects.filter(category_id=c, date__year=year, date__month=month).aggregate(
                    Sum('gastos', output_field=FloatField()))
                name = Categoria.objects.filter(id=c)
                data.append({
                    'name': str(name[0]),
                    'y': variable["gastos__sum"]
                })
            # Se obtiene el total del monto de los gastos ingresados.
            for d in data:
                total += d['y']
        except:
            pass

        return data, total

    # Metodo para obtener la información de la grafica a traves de filtros y el calendario que se gardara en una lista.
    def porcentaje_gastos_anuales(self):
        data = []
        total = 0
        year = datetime.now().year
        # Validación para traer los id de las categorias creadas por cada usuario.
        try:
            Catego = Categoria.objects.all().values_list('id', flat=True)
            # Ciclo para filtrar la información por las categorias y los años.
            for c in Catego:
                variable = informes.objects.filter(category_id=c, date__year=year).aggregate(
                    Sum('gastos', output_field=FloatField()))
                name = Categoria.objects.filter(id=c)
                data.append({
                    'name': str(name[0]),
                    'y': variable["gastos__sum"]
                })
            # Se obtiene el total del monto de los gastos ingresados.
            for d in data:
                total += d['y']
        except:
            pass
        return data, total

    # Metodo para obtener la información de la grafica a traves de filtros y el calendario que se gardara en una lista.
    def porcentaje_presupuestos_semanales(self):
        data = []
        totalP = 0
        year = datetime.now().year
        month = datetime.now().month
        w = week(datetime(datetime.now().year, datetime.now().month, datetime.now().day))
        Catego = Categoria.objects.all().values_list('id', flat=True)
        # Ciclo para filtrar la información por las categorias y los años.
        for c in Catego:
            variable = informes.objects.filter(category_id=c, date__year=year, date__month=month,
                                               semana=w).aggregate(Sum('presupuesto', output_field=FloatField()))
            name = Categoria.objects.filter(id=c)
            data.append({
                'name': str(name[0]),
                'y': variable["presupuesto__sum"]
            })
        # Se obtiene el total del monto de los presupuestos ingresados.
        for d in data:
            if d['y'] is None:
                pass
            else:
                totalP += d['y']
        return data, totalP

    # Metodo para obtener la información de la grafica a traves de filtros y el calendario que se gardara en una lista.
    def porcentaje_presupuestos_mensuales(self):
        data = []
        totalP = 0
        year = datetime.now().year
        month = datetime.now().month
        Catego = Categoria.objects.all().values_list('id', flat=True)

        # Ciclo para filtrar la información por las categorias y los años.
        for c in Catego:
            variable = informes.objects.filter(category_id=c, date__year=year, date__month=month).aggregate(
                Sum('presupuesto', output_field=FloatField()))
            name = Categoria.objects.filter(id=c)
            data.append({
                'name': str(name[0]),
                'y': variable["presupuesto__sum"]
            })
        # Se obtiene el total del monto de los presupuestos ingresados.
        for d in data:
            if d['y'] is None:
                pass
            else:
                totalP += d['y']
        return data, totalP

    # Metodo para obtener la información de la grafica a traves de filtros y el calendario que se gardara en una lista.
    def porcentaje_presupuestos_anuales(self):
        data = []
        totalP = 0
        year = datetime.now().year
        Catego = Categoria.objects.all().values_list('id', flat=True)

        # Ciclo para filtrar la información por las categorias y los años.
        for c in Catego:
            variable = informes.objects.filter(category_id=c, date__year=year).aggregate(
                Sum('presupuesto', output_field=FloatField()))
            name = Categoria.objects.filter(id=c)
            data.append({
                'name': str(name[0]),
                'y': variable["presupuesto__sum"]
            })
        # Se obtiene el total del monto de los presupuestos ingresados.
        for d in data:
            if d['y'] is None:
                pass
            else:
                totalP += d['y']
        return data, totalP

    # Metodo post para enviar la información de cada una de las graficas de esta app.
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

    # Metodo para enviar la información al template
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

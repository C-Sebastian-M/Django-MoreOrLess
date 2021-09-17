from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.metas.forms import MetasForm, MetaForm
from core.metas.models import Metas
from core.gastos.models import Gastos
from core.categorias.models import Categoria
from django.db.models import FloatField, Sum


# Create your views here.
class MetasListView(ListView):
    model = Metas
    template_name = 'metas.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = None
        return super().dispatch(request, *args, **kwargs)

    """def suma_metas(self, f_c_m, date, categoria_id):
        total = 0
        for i in range(date.day, f_c_m.day):
            variable = Metas.objects.filter(category_id=categoria_id,
                                               date__year=f_c_m.year,
                                               date__month=f_c_m.month,
                                              date__day=i).aggregate(Sum('amount_meta', output_field=FloatField()))
            if variable['amount_meta__sum']==None:
                continue
            else:
                total+=variable['amount_meta__sum']

        return total"""

    """def metas(self):
        valores_metas = Metas.objects.all()
        porcentaje_list = []
        id = []
        fcm = []
        categoria = []
        amount = []
        date = []
        for v in valores_metas:
            gastos = self.suma_metas(v.f_c_m, v.date, v.category_id)
            porcetaje=(100*gastos)/v.amount
            porcentaje_list.append(int(porcetaje))
            id.append(v.id)
            fcm.append(v.f_c_m)
            obj = Categoria.objects.get(pk=v.category_id)
            categoria.append(obj)
            date.append(v.date)
            amount.append(v.amount)
        print(porcentaje_list)
        gastos = zip(id,fcm,categoria,date, amount,porcentaje_list)
        return gastos"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        """context['metas'] = self.metas()"""
        return context


class MetasCreateView(CreateView):
    model = Metas
    form_class = MetasForm
    template_name = 'form_metas.html'
    success_url = reverse_lazy('metas')

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
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
        context['title'] = 'Ingresar meta'
        context['list_url'] = reverse_lazy('metas')
        context['action'] = 'add'
        return context


class MetasUpdateView(UpdateView):
    model = Metas
    form_class = MetasForm
    template_name = 'form_metas.html'
    success_url = reverse_lazy('metas')

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
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
        context['title'] = 'Editar categoria'
        context['list_url'] = reverse_lazy('metas')
        context['action'] = 'edit'

        return context


class MetasDeleteView(DeleteView):
    model = Metas
    template_name = 'delete_metas.html'
    success_url = reverse_lazy('metas')

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
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
        context['title'] = 'Eliminar meta'
        context['list_url'] = reverse_lazy('metas')
        return context


class MetaUpdateView(UpdateView):
    model = Metas
    form_class = MetaForm
    template_name = 'form_metas.html'
    success_url = reverse_lazy('metas')

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.progesoMeta()
        """self.fechas()"""
        return super().dispatch(request, *args, **kwargs)

    def progesoMeta(self):
        metas = Metas.objects.filter(id=self.object.id)
        print(metas)
        for c in metas:
            print(c.category_id)

    def fechas(self):
        valores_metas = Metas.objects.all()

        for v in valores_metas:
            date = v.date
            fcm = v.f_c_m
            print (date, fcm)


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
        context['title'] = 'Ingresar dinero a la meta'
        context['list_url'] = reverse_lazy('metas')
        context['action'] = 'edit'
        return context

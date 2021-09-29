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


# Create your views here.
class MetasListView(ListView):
    model = Metas
    template_name = 'metas.html'

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(user_creation_id=user)

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        valores_meta = Metas.objects.filter(user_creation_id=user).aggregate(total_meta=Sum('amount'))
        print(valores_meta)
        return super().dispatch(request, *args, **kwargs)

    def metas(self):
        user = self.request.user
        valores_metas = Metas.objects.all()
        Catego = Metas.objects.all().values_list('id', flat=True)
        porcentaje = []
        for c in Catego:
            variable = AmountMetas.objects.filter(user_creation_id=user, meta_id=c)
            total = 0
            for v in variable:
                if v is None:
                    continue
                else:
                    total+=v.amount
            porcentaje.append(total)

        id, gastos, category_id, f_c_m, date = [], [], [], [], []

        for v in valores_metas:
            id.append(v.id)
            gastos.append(v.amount)
            obj = Categoria.objects.get(pk=v.category_id)
            category_id.append(obj)
            f_c_m.append(v.f_c_m)
            date.append(v.date)

        barra = []
        for i in range(len(gastos)):
            barra.append(int(porcentaje[i]*100/gastos[i]))
        print(barra)

        metas = zip(id, gastos, category_id, f_c_m, date, barra)
        return metas


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['metas'] = self.metas()
        return context


class MetasCreateView(CreateView):
    model = Metas
    form_class = MetasForm
    template_name = 'form_metas.html'
    success_url = reverse_lazy('metas')

    def get_form_kwargs(self):
        kwargs = super(MetasCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user.id})
        return kwargs

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(user_creation_id=user)

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


class AmountMetaCreateView(CreateView):
    model = AmountMetas
    form_class = MetaForm
    template_name = 'form_metas.html'
    success_url = reverse_lazy('metas')

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = None
        model = self.kwargs['pk']

        return super().dispatch(request, *args, **kwargs)



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
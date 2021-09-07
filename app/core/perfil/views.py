from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, UpdateView
from core.perfil.forms import PerfilForm
from core.perfil.models import PerfilModel



# Create your views here.


class PerfilListView(ListView):
    model = PerfilModel
    template_name = 'perfil.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['index_url'] = reverse_lazy('index')
        return context


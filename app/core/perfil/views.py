from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, UpdateView
from core.perfil.models import PerfilModel



# Create your views here.

#Aquí van a estar el listview
class PerfilListView(ListView):
    # Especificación del modelo donde se guardara la información
    model = PerfilModel
    # Especificación del template html que vamos a utilizar
    template_name = 'perfil.html'

    # Metodo de seguridad
    @method_decorator(csrf_exempt)
    # Metodo para requerir estar logeado
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['index_url'] = reverse_lazy('index')
        return context


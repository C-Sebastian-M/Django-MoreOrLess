from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

#Llamando a la pagina principal
class IndexView(TemplateView):
    template_name = 'index.html'

    # Metodo de seguridad
    @method_decorator(csrf_exempt)
    # Metodo para requerir estar logeado
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = None
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['index_url'] = reverse_lazy('index')
        return context

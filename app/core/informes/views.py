from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from core.informes.models import informes

# Create your views here.


class InformesListView(ListView):
    model = informes
    template_name = 'informes.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['index_url'] = reverse_lazy('index')
        return context
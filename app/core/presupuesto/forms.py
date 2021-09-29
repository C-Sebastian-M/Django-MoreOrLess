from django.forms import *

from core.categorias.models import Categoria
from core.presupuesto.models import Presupuesto


class PresupuestoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(PresupuestoForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset =Categoria.objects.filter(user_creation_id=user)

    class Meta:
        model = Presupuesto
        fields = '__all__'
        exclude = ('date','user_creation',)
        labels = {
            'amount': 'Monto',
            'category': 'Categoria',
        }
        widgets = {
            'amount': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el monto del presupuesto',
                }
            ),
             'category': Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Categoria',
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
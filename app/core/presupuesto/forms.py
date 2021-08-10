from django.forms import *
from core.presupuesto.models import Presupuesto


class PresupuestoForm(ModelForm):
    class Meta:
        model = Presupuesto
        fields = '__all__'
        exclude = ('date',)
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

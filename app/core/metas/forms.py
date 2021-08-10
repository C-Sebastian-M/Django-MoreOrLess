from django.forms import *

from core.gastos.models import Gastos
from core.metas.models import Metas


class MetasForm(ModelForm):
    class Meta:
        model = Metas
        fields = '__all__'
        exclude = ('date',)
        labels ={
            'f_c_m':'Fecha en la que deseas cumplir tu meta',
            'valor': 'Monto',
            'category':'Categoria',
        }

        widgets = {
            'f_c_m': DateInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'category': Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'amount': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el monto de la meta',
                }
            ),
        }

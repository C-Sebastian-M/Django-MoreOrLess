from django.forms import *

from core.categorias.models import Categoria
from core.gastos.models import *




class GastosForm(ModelForm):
    class Meta:
        model = Gastos
        fields = '__all__'
        exclude = ('date',)
        labels ={
            'amount':'Monto',
            'category':'Categoria',
        }

        widgets = {
            'amount': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el monto del gasto',
                }
            ),
            'category': TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }

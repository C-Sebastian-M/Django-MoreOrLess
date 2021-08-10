from django.forms import *

from core.gastos.models import Gastos


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
            'category': Select(
                attrs={
                    'class': 'form-control'
                }
            ),
        }

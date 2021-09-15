from django.forms import *
from core.gastos.models import *


class GastosForm(ModelForm):
    class Meta:
        model = Gastos
        fields = '__all__'
        exclude = ('date','semana')
        labels = {
            'amount': 'Monto',
            'category': 'Categoria',
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

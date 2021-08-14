from django.forms import *

from core.categorias.models import Categoria
from core.metas.models import Metas


class MetasForm(ModelForm):
    class Meta:
        model = Metas
        fields = '__all__'
        exclude = ('date',)
        labels = {
            'f_c_m': 'Fecha en la que deseas cumplir tu meta',
            'valor': 'Monto',
            'category': 'Categoria',
        }

        widgets = {
            'f_c_m': DateInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'category': TextInput(
                attrs={
                    'class': 'form-control select2',
                }
            ),
            'amount': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el monto de la meta',
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

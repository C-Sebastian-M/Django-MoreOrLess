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
            'category': TextInput(
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
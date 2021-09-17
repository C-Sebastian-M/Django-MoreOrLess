from django.forms import *
from core.metas.models import Metas
from core.categorias.models import Categoria



class MetasForm(ModelForm):
    class Meta:
        model = Metas
        fields = '__all__'
        exclude = ('date','amount_meta')
        labels = {
            'f_c_m': 'Fecha en la que deseas cumplir tu meta',
            'valor': 'Monto',
            'category': 'Categoria',
        }

        widgets = {
            'f_c_m': DateInput(
                attrs={
                    'class': 'form-control datetimepicker-input',
                    'type' : 'date',
                }
            ),
            'category': Select(
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

class MetaForm(ModelForm):
    class Meta:
        model = Metas
        fields = 'amount_meta',
        labels = {
            'amount_meta' : 'Añadir dinero a la meta'
        }

        widgets = {
            'amount_meta': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el dinero a añadir a la meta',
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

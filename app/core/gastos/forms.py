from django.forms import *
from core.gastos.models import *


class GastosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(GastosForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset =Categoria.objects.filter(user_creation_id=user)

    class Meta:

        model = Gastos
        fields = '__all__'
        exclude = ('date','semana','user_creation',)
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

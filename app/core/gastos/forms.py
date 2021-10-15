from django.forms import *
from core.gastos.models import *


# Formulario de ingreso de datos de la aplicacion Gastos.
class GastosForm(ModelForm):
    # Funcion Init para obtener el usuario y mostrar las categorias creadas por el usuario.
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(GastosForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Categoria.objects.filter(user_creation_id=user)

    class Meta:
        # Especificacion del modelo al cual se le ingresaran datos
        model = Gastos
        # Cuales son los campos de ingreso de datos
        fields = '__all__'
        # Exclusion de campos de la base de datos que no serán mostrados al usuario
        exclude = ('date', 'semana', 'user_creation',)
        # Campos de ingreso de datos, con su texto que sera mostrado
        labels = {
            'amount': 'Monto',
            'category': 'Categoria',
        }
        # Atributos de los campos de ingreso de datos
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

    # Funcion de guardado de la información
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

from django.forms import *
from core.categorias.models import Categoria
from core.presupuesto.models import Presupuesto


# Formulario de ingreso de datos de la aplicacion presupuesto.
class PresupuestoForm(ModelForm):
    # Funcion Init para obtener el usuario y mostrar las categorias creadas por el usuario.
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(PresupuestoForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Categoria.objects.filter(user_creation_id=user)

    class Meta:
        # Especificacion del modelo al cual se le ingresaran datos
        model = Presupuesto
        # Cuales son los campos de ingreso de datos
        fields = '__all__'
        # Exclusion de campos de la base de datos que no serán mostrados al usuario
        exclude = ('date', 'user_creation',)
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

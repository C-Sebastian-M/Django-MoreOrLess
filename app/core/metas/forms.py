from django.forms import ModelForm, DateInput, Select, TextInput
from core.categorias.models import Categoria
from core.metas.models import Metas, AmountMetas


# Formulario de ingreso de datos de la aplicacion metas
class MetasForm(ModelForm):
    # Funcion Init para obtener el usuario, y mostrar las categorias creadas por el usuario
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(MetasForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Categoria.objects.filter(user_creation_id=user)

    class Meta:
        # Especificacion del modelo al cual se le ingresaran datos
        model = Metas
        # Cuales son los campos de ingreso de datos
        fields = '__all__'
        # Exclusion de campos de la base de datos que no serán mostrados al usuario
        exclude = ('date', 'amount_meta', 'user_creation')
        # Campos de ingreso de datos, con su texto que sera mostrado
        labels = {
            'f_c_m': 'Fecha en la que deseas cumplir tu meta',
            'valor': 'Monto',
            'category': 'Categoria',
        }
        # Atributos de los campos de ingreso de datos
        widgets = {
            'f_c_m': DateInput(
                attrs={
                    'class': 'form-control datetimepicker-input',
                    'type': 'date',
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


# Clase del formulario de ingreso de datos a la meta
class MetaForm(ModelForm):
    class Meta:
        # Especificación del modelo donde se ingresaran datos
        model = AmountMetas
        # Campos de ingreso de datos que seran mostrados
        fields = 'amount',
        # Campos de ingreso de datos, con su texto que sera mostrado
        labels = {
            'amount': 'Añadir dinero a la meta'
        }
        # Atributos de los campos de ingreso de datos
        widgets = {
            'amount': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el dinero a añadir a la meta',
                }
            ),
        }

    # Funcion de guardado del formulario.
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

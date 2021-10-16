from django.forms import *
from core.categorias.models import Categoria

#Formulario de registro de categorias
class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        # Para que traiga todos los elementos de los modelos categoria
        fields = '__all__'
        #Para que se excluya el usuario el usuario que creó la categoria, para una discriminación de usuario
        exclude = ('user_creation',)
        # Configuramos el campo category para que se muestre el texto Nueva categoria
        labels = {
            'category': 'Nueva categoria',
        }
        #Atributos al campo de category personalizados
        widgets = {
            'category': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Pon el nombre de la categoria que deseas crear',
                }
            ),
        }

    # Función para guardar información y aceptación de errores
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

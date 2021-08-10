from django.forms import *

from core.categorias.models import Categoria
from core.presupuesto.models import Presupuesto


class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        labels = {
            'category': 'Categoria',
        }
        widgets = {
            'category': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Pon el nombre de la categoria que deseas crear',
                }
            ),
        }

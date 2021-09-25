from django.forms import *
from core.categorias.models import Categoria

class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        exclude = ('user_creation',)
        labels = {
            'category': 'Nueva categoria',
        }
        widgets = {
            'category': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Pon el nombre de la categoria que deseas crear',
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

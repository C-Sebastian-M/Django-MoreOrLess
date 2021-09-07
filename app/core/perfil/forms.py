from django.contrib.auth.forms import UserCreationForm
from django.forms import *
from core.perfil.models import *


class PerfilForm(ModelForm):
    class Meta:
        model = PerfilModel
        fields = '__all__'
        labels = {
            'image' : 'Imagen de perfil',
        }
        widgets = {
            'image' : FileInput(
                attrs={
                    'class': 'form-control',
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
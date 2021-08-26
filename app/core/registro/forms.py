from django.contrib.auth.forms import UserCreationForm
from django.forms import *

from core.presupuesto.models import Presupuesto
from core.registro.models import Registro


class RegistroForm(UserCreationForm):
    class Meta:
        model = Registro
        fields = 'first_name', 'last_name','email','username', 'password1', 'password2'

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
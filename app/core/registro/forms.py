from django.contrib.auth.forms import UserCreationForm
from core.registro.models import RegistroUsuario


class RegistroUsuariosForm(UserCreationForm):
    class Meta:
        model = RegistroUsuario
        fields = 'first_name','last_name','username','email'

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

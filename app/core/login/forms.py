from django import forms
from core.registro.models import RegistroUsuario


class ResetPasswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Ingrese su username',
        'class' : 'form-control',
        'autocomplete':'off'
    }))

    def clean(self):
        cleaned = super().clean()
        if not RegistroUsuario.objects.filter(username=cleaned['username']).exists():
            self.errors['error'] = self.errors.get('Error', self.error_class())
            self.errors['error'].append('el nombre de usuario no existe')
        return cleaned

    def get_user(self):
        username = self.cleaned_data.get('username')
        return RegistroUsuario.objects.get(username=username)

class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Nueva contraseña',
        'class' : 'form-control',
        'autocomplete':'off'
    }))

    confirmPassword = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirmar contraseña',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def clean(self):
        cleaned = super().clean()
        password = cleaned['password']
        confirmPassword = cleaned['confirmPassword']
        if password != confirmPassword:
            self.errors['error'] = self.errors.get('Error', self.error_class())
            self.errors['error'].append('Las contraseñas no coinciden')
        return cleaned
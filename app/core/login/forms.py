from django import forms
from core.registro.models import RegistroUsuario

#Formulario del reseteo de contraseña
class ResetPasswordForm(forms.Form):
    #Atributos que trae el atributo username
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Ingrese su username',
        'class' : 'form-control',
        'autocomplete':'off'
    }))
    #Funcion para validar si el usuario existe o no
    def clean(self):
        cleaned = super().clean()
        if not RegistroUsuario.objects.filter(username=cleaned['username']).exists():
            self.errors['error'] = self.errors.get('Error', self.error_class())
            self.errors['error'].append('el nombre de usuario no existe')
        return cleaned
    #Funcion para obtener el usuario
    def get_user(self):
        username = self.cleaned_data.get('username')
        return RegistroUsuario.objects.get(username=username)
#Formulario del cambio de contraseña
class ChangePasswordForm(forms.Form):
    #Atributos del campo de contraseña
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Nueva contraseña',
        'class' : 'form-control',
        'autocomplete':'off'
    }))
    # Atributos del campo de confirmacion contraseña
    confirmPassword = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirmar contraseña',
        'class': 'form-control',
        'autocomplete': 'off'
    }))
    #Funcion para validar si las dos contraseñas ingresadas, coinciden
    def clean(self):
        cleaned = super().clean()
        password = cleaned['password']
        confirmPassword = cleaned['confirmPassword']
        if password != confirmPassword:
            self.errors['error'] = self.errors.get('Error', self.error_class())
            self.errors['error'].append('Las contraseñas no coinciden')
        return cleaned
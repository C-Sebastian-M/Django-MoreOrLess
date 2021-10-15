from django.contrib.auth.forms import UserCreationForm
from core.registro.models import RegistroUsuario

#Formulario de registro utilizando propiedades de la clase UserCreationForm dada por el framework
class RegistroUsuariosForm(UserCreationForm):
    class Meta:
        #Especificación del modelo donde se guardara la información en la base de datos
        model = RegistroUsuario
        #Estos son los campos que se van a mostrar en el formulario
        fields = 'first_name', 'last_name', 'username', 'email','image',
        #Configuramos el campo image para que se muestre el texto Imagen de perfil
        labels = {
            'image':'Imagen de perfil (opcional)'
        }

    #Función para guardar información
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

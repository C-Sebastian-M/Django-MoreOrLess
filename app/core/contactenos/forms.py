from django.forms import *
from core.contactenos.models import ContactUs


class ContactForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'campo-tab-err'

    class Meta:
        model = ContactUs
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'id': 'name',
                    'class': 'campo-tab-err',
                    'placeholder': 'Ingresa tu Nombre',
                }
            ),
            'email': EmailInput(
                attrs={
                    'id': 'email',
                    'class': 'campo-tab-err',
                    'placeholder': 'Email@hotmail.com'
                }
            ),

            'message': Textarea(
                attrs={
                    'name': 'message',
                    'id': 'message',
                    'cols': '30',
                    'rows': '5',
                    'class': 'campo-tab-err'
                }
            )
        }

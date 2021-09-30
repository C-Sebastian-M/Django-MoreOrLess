# from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from core.contactenos.forms import ContactForm
from core.contactenos.models import ContactUs
from django.urls import reverse_lazy

# Emails
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.

class ContactMore(TemplateView):
    template_name = 'contact_us.html'


class ContactView(CreateView):
    model = ContactUs
    form_class = ContactForm
    template_name = 'contact_us.html'
    success_url = reverse_lazy('contactenos')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        email_from = settings.EMAIL_HOST_USER
        mensaje = 'Nombre de usuario: ' + form.cleaned_data.get('name') + '\n' + 'Correo del usuario: ' \
                  + form.cleaned_data.get('email') + '\n' + '\n' + 'Mensaje: ' + \
                  '\n' + '\n' + form.cleaned_data.get('message')
        send_mail(
            subject='Reporte:',
            message=mensaje,
            from_email=email_from,
            recipient_list=["moreorless.project@gmail.com"],
        )
        return HttpResponseRedirect(self.get_success_url() + "?ok")

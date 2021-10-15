import smtplib
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib.auth.views import LoginView
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView

from config import settings
from core.login.forms import ResetPasswordForm, ChangePasswordForm
from core.registro.models import RegistroUsuario


# Vista para el login del usuario a la pagina, dada por la clase LoginView del framework que permite el login
class LoginFormView(LoginView):
    # Plantilla html para la visualización de la pantalla
    template_name = 'login.html'

    # Metodo de seguridad
    @method_decorator(csrf_exempt)
    # Metodo dispatch, validando si el usuario esta autentificado para redirigirlo a la pantalla del index
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesión'
        return context


# Vista de reseteo de contraseña
class ResetPasswordView(FormView):
    # La clase de formulario que vamos a mostrar para los campos de ingreso de datos
    form_class = ResetPasswordForm
    # Plantilla html para mostrar la información de la pagina y todos los componente front-end
    template_name = 'olvido-contraseña.html'
    # Url de redireccion
    success_url = reverse_lazy('login')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # Envio de email para el reseteo de contraseña
    def send_email_reset_pwd(self, user):
        data = {}
        try:
            # Url de nuestro dominio
            URL = settings.DOMAIN if not settings.DEBUG else self.request.META['HTTP_HOST']

            # Generación de token con el metodo uuid.uuid4, para darle auditoria a nuestro reseteo de contrasela
            user.token = uuid.uuid4()
            # Guardar el token en la base de datos
            user.save()

            # De donde vamos a enviar nuestro email
            mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            mailServer.starttls()
            # A donde vamos a mandar el email
            mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            # Email al correo que registro el usuario
            email_to = user.email

            mensaje = MIMEMultipart()
            # Configuración del envio del correo
            mensaje['From'] = settings.EMAIL_HOST_USER
            mensaje['To'] = email_to
            mensaje['Subject'] = 'Reseteo de contraseña'
            # Contenido del correo
            content = render_to_string('send_email.html',
                                       # Configuración que vamos a enviar en nuestro HTML para el usuario
                                       {'user': user,
                                        'link_resetpwd': 'http://{}/change/password/{}/'.format(URL, str(user.token)),
                                        'link_home': 'http://{}'.format(URL)})
            mensaje.attach(MIMEText(content, 'html'))

            mailServer.sendmail(settings.EMAIL_HOST_USER, email_to, mensaje.as_string())

        except Exception as e:
            data['error'] = str(e)
        return data

    # Metodo post para guardar la información, en este caso, enviar el correo.
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                user = form.get_user()
                data = self.send_email_reset_pwd(user)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reseteo de contraseña'
        return context


# Vista de cambio de contraseña
class ChangePasswordView(FormView):
    # Clase de formulario que vamos a mostrar para los campos de ingreso de datos
    form_class = ChangePasswordForm
    # Plantilla html para mostrar al usuario los campos y el front end de nuestro proyecto
    template_name = 'recuperar-contraseña.html'
    # Url de redireccion al completar los campos de nuestro formulario
    success_url = reverse_lazy('login')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # Obtenemos el token del usuario para saber si ya se utilizo por medio de la validación if
    def get(self, request, *args, **kwargs):
        token = self.kwargs['token']
        if RegistroUsuario.objects.filter(token=token).exists():
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect(self.success_url)

    # Metodo post para guardar la información al cambio de contraseña
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                user = RegistroUsuario.objects.get(token=self.kwargs['token'])
                user.set_password(request.POST['password'])
                user.token = uuid.uuid4()
                user.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva contraseña'
        context['list_url'] = 'login'
        return context

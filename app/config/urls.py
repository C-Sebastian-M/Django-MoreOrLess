"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.homepage.views import IndexView

#Urls que estamos utilizando para nuestro aplicativo según las plicaciones que tenemos
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name="index"),
    path('', include('core.login.urls')),
    path('', include('core.registro.urls')),
    path('', include('core.presupuesto.urls')),
    path('', include('core.metas.urls')),
    path('', include('core.gastos.urls')),
    path('', include('core.informes.urls')),
    path('', include('core.perfil.urls')),
    path('', include('core.categorias.urls')),
    path('', include('core.contactenos.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

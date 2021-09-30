from django.urls import path

from core.contactenos.views import ContactView

urlpatterns = [
    path('contactenos/', ContactView.as_view(), name="contactenos"),

]

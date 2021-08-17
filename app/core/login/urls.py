from django.urls import path

from core.login.views import LoginFormView

urlpatterns = [
    path('login/', LoginFormView.as_view(), name='login'),
]

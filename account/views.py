from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views.generic import CreateView
from .forms import UserRegistrationForm


class MySignupView(CreateView):
    form_class = UserRegistrationForm
    success_url = 'login'
    template_name = 'account/register.html'


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'account/login.html'

from django.urls import path
from django.contrib.auth.views import LogoutView


from .views import *

urlpatterns = [
    path('login', MyLoginView.as_view(), name='login'),
    path('register', MySignupView.as_view()),
    path('logout', LogoutView.as_view(), name='logout')
]
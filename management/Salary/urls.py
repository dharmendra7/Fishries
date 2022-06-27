from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='userSignUp'),
    path('signin/', LoginView.as_view(), name='userSignIn'),
    path('sendOTP/', SendOTPView.as_view(), name='SendOTP'),
]
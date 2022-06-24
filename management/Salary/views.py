from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from .serializers import *
from .models import *
from common.utils.views import *
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import AllowAny

# Create your views here.

class RegisterView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_class = [AllowAny,] 


    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=False)
            if serializer.is_valid():
                serializer.save()
                user_data = serializer.data
                user = User.objects.get(email=user_data['email'])
                
                response_data = {
                    'mobile_number': user.mobile_numer,
                    'email': user.email,
                    'refreshToken': user.tokens()['refresh'],
                    'accessToken': user.tokens()['access'],
                    'firstname': user.first_name,
                    'lastname': user.last_name,
                }

                return send_response(request, code= 200, message='SignUp success', data=response_data)
            else:
                error_msg_value = list(serializer.errors.values())[0]
                print(error_msg_value)
                return send_response_validation(request, code=2001, message = _(error_msg_value[0]))    
        
        except Exception as e:
            return send_response_validation(request, code=500, message = str(e))  
        
# class LoginView()
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.http import HttpResponse
from .serializers import *
from .models import *
from common.utils.views import *
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

import random
from twilio.rest import Client
# Create your views here.

headerAuthParam = [OpenApiParameter(
    name='Authorization', location=OpenApiParameter.HEADER,
    type=OpenApiTypes.STR,
    description='Authorization',
    required=True,
    default='Bearer ',
),]

# headerParam = [OpenApiParameter(
#     name='Link', 
#     location=OpenApiParameter.HEADER,
#     type=OpenApiTypes.STR,
#     description='Paste your link here',
#     required=True,
# ),]

class RegisterView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_class = [AllowAny,] 

    @extend_schema(
        responses = {
            200:UserLoginResponse(),
            400:commonErrorResponse()
        }
    )
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=False)
            if serializer.is_valid():
                serializer.save()
                user_data = serializer.data
                user = User.objects.get(email=user_data['email'])
                
                response_data = {
                    'firstname': user.first_name,
                    'lastname': user.last_name,
                    'mobile_number': user.mobile_numer,
                    'email': user.email,
                    'refreshToken': user.tokens()['refresh'],
                    'accessToken': user.tokens()['access'],
                }

                return send_response(request, code= 200, message='SignUp success', data=response_data)
            else:
                error_msg_value = list(serializer.errors.values())[0]
                print(error_msg_value)
                return send_response_validation(request, code=2001, message = _(error_msg_value[0]))    
        
        except Exception as e:
            return send_response_validation(request, code=500, message = str(e))  
        
class LoginView(generics.GenericAPIView):
    # queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        responses={
            200:UserLoginResponse(),
            400:commonErrorResponse()
        }
    )
    def post(self, request):
        try:
            serializer = self.serializer_class(data= request.data, context = {'request':request})
            if serializer.is_valid():
                user = User.objects.get(mobile_numer = request.data['mobile_numer'])
                
                response_data = {
                        'firstname': user.first_name,
                        'lastname': user.last_name,
                        'mobile_number': user.mobile_numer,
                        'email': user.email,
                        'refreshToken': user.tokens()['refresh'],
                        'accessToken': user.tokens()['access'],
                    }
                return send_response(request, code= 200, message = 'SignIn success', data = response_data)

            else:
                error_msg_value = list(serializer.errors.values())[0]
                return send_response_validation(request, code=2001, message = _(error_msg_value[0])) 

        except Exception as e:
            return send_response_validation(request, code=500, message = str(e))

class SendOTPView(generics.GenericAPIView):
    queryset = User.objects.all()
    permission_class = (IsAuthenticated,)

    @extend_schema(
        parameters=headerAuthParam,
    )
    def post(self , request):
        try:
            userAuthentication = isUserAuth(self.request)
            print(userAuthentication)
            if userAuthentication != True:
                return send_response_validation(request, code=403, message= userAuthentication)

            
            number = random.randint(1111,9999)  
            userdata = self.request.user
            userdata.otp=number
            account_sid = settings.TWILIO_ACCOUNT_SID
            auth_token = settings.TWILIO_AUTH_TOKEN
            client = Client(account_sid, auth_token)
            print(userdata.otp)
            message = client.messages.create(
                                            body=f'Hi, your OTP is {number}.',
                                            from_='+19036485904',
                                            to = '+91' + userdata.mobile_numer )

            userdata.save()
            return send_response_validation(request, code=200, message= _("OTP sent successfully"))

        except Exception as e:
            return send_response_validation(request, code=500, message = str(e))
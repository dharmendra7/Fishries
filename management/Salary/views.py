from django.shortcuts import render
from .serializers import *
from .models import *
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import AllowAny

# Create your views here.

class RegisterView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_class = [AllowAny,] 


    def post(self, request):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=False)
        return HttpResponse("hello")
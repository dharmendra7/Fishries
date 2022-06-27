from rest_framework import serializers
from .models import *


class CreateUserSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(read_only = True)
    class Meta:
        model = User
        fields = ('first_name','last_name', 'email', 'password', 'mobile_numer', 'alternate_number', 'district', 'deviceType', 'deviceToken', 'deviceName','deviceOs','deviceId')
        extra_kwargs = {'password': {'write_only': True}}

    def __init__(self, *args, **kwargs):
        super(CreateUserSerializer,self).__init__(*args, **kwargs)
        self.fields['first_name'].error_messages['blank'] = u'First name field cannot be blank'
        self.fields['first_name'].error_messages['required'] = u'The first name field is required'
        self.fields['last_name'].error_messages['blank'] = u'Last name field cannot be blank'
        self.fields['last_name'].error_messages['required'] = u'The Last name field is required'
        self.fields['email'].error_messages['blank'] = u'Email field cannot be blank'
        self.fields['email'].error_messages['required'] = u'Email field is required'
        self.fields['password'].error_messages['blank'] = u'Password field cannot be blank'
        self.fields['password'].error_messages['required'] = u'Password field is required'
        self.fields['mobile_numer'].error_messages['blank'] = u'Mobile Number field cannot be blank'
        self.fields['mobile_numer'].error_messages['required'] = u'Mobile Number field is required'
        self.fields['district'].error_messages['blank'] = u'District field cannot be blank'
        self.fields['district'].error_messages['required'] = u'District field is required'

    def validate(self, attrs):
        email = attrs.get('email', '')
        mobile_number = attrs.get('mobile_numer', '')

        if User.objects.filter(mobile_numer=mobile_number).exists():
            raise serializers.ValidationError("Mobile number already in use")

        # if User.objects.filter(email=email).exists():
        #     raise serializers.ValidationError("Email already in use")

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
        email=validated_data['email'],
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name'],
        password=validated_data['password'],
        mobile_numer=validated_data['mobile_numer'],
        alternate_number=validated_data['alternate_number'],
        district=validated_data['district'],
        deviceType=validated_data['deviceType'],
        deviceToken=validated_data['deviceToken'],
        deviceName=validated_data['deviceName'],
        deviceOs=validated_data['deviceOs'],
        deviceId=validated_data['deviceId'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
        # user = User.objects.create_user(**validatecurrent_seasond_data)
        # print(user)
        # return user

class LoginResponseSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    mobile_number = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    refreshToken = serializers.CharField(required=False)
    accessToken = serializers.CharField(required=False)
    
class UserLoginResponse(serializers.Serializer):
    responseCode = serializers.IntegerField()
    responseMessage = serializers.CharField()
    responseData = LoginResponseSerializer()

class commonErrorResponse(serializers.Serializer):
    responseCode = serializers.IntegerField()
    responseMessage = serializers.CharField()

class LoginSerializer(serializers.ModelSerializer):
    mobile_numer = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ('mobile_numer','district', 'deviceType', 'deviceToken', 'deviceName','deviceOs','deviceId')
        # extra_kwargs = {'password': {'write_only': True}}

    def __init__(self, *args, **kwargs):
        super(LoginSerializer,self).__init__(*args, **kwargs)
        self.fields['mobile_numer'].error_messages['blank'] = u'Mobile number cannot be blank'
        self.fields['mobile_numer'].error_messages['required'] = u'Mobile Number field is required'
        # self.fields['password'].error_messages['blank'] = u'Password field cannot be blank'
        # self.fields['password'].error_messages['required'] = u'Password field is required'
        self.fields['district'].error_messages['blank'] = u'District field cannot be blank'
        self.fields['district'].error_messages['required'] = u'District field is required'

    def get_refreshToken(self, obj):
        user = User.objects.get(mobile_numer=obj['mobile_numer'])
        return user.tokens()['refresh']

    def get_accessToken(self, obj):
        user = User.objects.get(mobile_numer=obj['mobile_numer'])
        return user.tokens()['access']

    def validate(self, attrs):
        if User.objects.filter(mobile_numer = attrs.get('mobile_numer','')).exists() is False: 
            raise serializers.ValidationError('Mobile number does not exist!!!')
        if User.objects.filter(district = attrs.get('district','')).exists() is False :
            raise serializers.ValidationError('Your district name is not same as you give during sign up')
        else:
            user = User.objects.get(mobile_numer = attrs.get('mobile_numer',''))
            return {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'mobile_numer':user.mobile_numer,
                'district':user.district,
            }

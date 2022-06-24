import time
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):

    ANDROID = 'android'
    IPHONE = 'iphone'

    phone_message = 'Phone number must start with either 9, 8, 7 or 6 and should enter in this format: 9999955555'
    phone_regex = RegexValidator(
    regex=r'^[6-9]\d{9}$',
    message=phone_message
    )
    ten_digit = '''-> Phone number should be of 10 digits <br/> 
    -> Phone number must starts with either 9, 8, 7 or 6 <br/>
    -> Should enter in this format: 9999955555
    '''
    mobile_numer =  models.CharField(max_length=12,null=False,unique=True, validators=[phone_regex],help_text=ten_digit)
    username = models.CharField(blank = True, max_length=255,unique=True,null=True)
    first_name = models.CharField(null = False, max_length = 255)
    last_name = models.CharField(null = False, max_length = 255)
    alternate_number = models.CharField(max_length=12,null=False, unique=True, validators=[phone_regex],help_text=ten_digit)
    email = models.EmailField(unique=True)
    district = models.CharField(max_length=255)
    otp = models.CharField(max_length=4, blank=True)
    deviceType = models.CharField(max_length=10, choices=((ANDROID,'Android'),(IPHONE,'iphone')), default='ANDROID')
    deviceToken = models.CharField(max_length=255, blank=True)
    deviceName = models.CharField(max_length=100, blank=True)
    deviceOs = models.CharField(max_length=100, blank=True)
    deviceId = models.CharField(max_length=100, blank=True)
    created_at = models.IntegerField(default = int(time.time()))
    updated_at = models.IntegerField(default = int(time.time()))

    def __str__(self):
        return self.first_name

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

class BoatDetails(models.Model):
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    boat_name = models.CharField(max_length = 255)
    boat_number = models.CharField(max_length = 255)
    created_at = models.IntegerField()
    updated_at = models.IntegerField()

class BoatMembers(models.Model):
    boat_id = models.ForeignKey(BoatDetails, on_delete=models.CASCADE)
    boat_member_name = models.CharField(max_length = 255)
    boat_member_role = models.CharField(max_length = 255)
    boat_member_salary = models.IntegerField()
    created_at = models.IntegerField()
    updated_at = models.IntegerField()

class WithdrawOfMember(models.Model):
    boat_member_id = models.ForeignKey(BoatMembers, on_delete = models.CASCADE)
    upar_amout = models.IntegerField()
    created_at = models.IntegerField()
    updated_at = models.IntegerField()

class LeaveOfMember(models.Model):
    boat_member_id = models.ForeignKey(WithdrawOfMember, on_delete = models.CASCADE)
    leave_start_date = models.DateTimeField(auto_now=False)
    leave_end_last = models.DateTimeField(auto_now=False)
from django.http import JsonResponse
import hmac
import hashlib
from django.utils import translation
from django.utils.translation import gettext_lazy as _
import requests
import json

def error_404(request, exception):
    message = 'Endpoint not found.'

    response = JsonResponse(data={'message': message, 'status_code': 404})
    response.status_code = 404
    return response

def error_500(request, exception):
    message = 'An internal error occurred. An administrator has been notified. '

    response = JsonResponse(data={'message': message, 'status_code': 500})
    response.status_code = 500
    return response

def send_response(request, code, message, data):

    response = JsonResponse(data={'responseCode': code, 'responseMessage': message, 'responseData': data})
    response.status_code = 200
    return response

def send_response_validation(request, code, message):

    response = JsonResponse(data={'responseCode': code, 'responseMessage': message})
    response.status_code = 200
    return response

def send_response_unauthorized(request, code, message):

    response = JsonResponse(data={'responseCode': code, 'responseMessage': message})
    response.status_code = 401
    return response


def validate_token(nonce, timestamp, token):

        secretKey = "w558XFrKN5Ue78eaLRsXSpe5zF9Q2jvC2b9DMM5r"
        privateKey = b"Hg1dhgKS1A1MT0AI5Pf5ydf7r6vlwgjUfa9s"

        secret_key = b"NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j"
        total_params = bytearray("nonce="+nonce+"&timestamp="+timestamp+"|"+secretKey,'utf-8')
        signature = hmac.new(privateKey, total_params, hashlib.sha256).hexdigest()

        if signature == token:
            return "valid"
        else:
            return "invalid"

def required_header(nonce, timestamp, token):

        if(len(nonce)<=1):
            return _("Header nounce filed is required")
        if(len(timestamp)<=1):
            return _("Header timestamp filed is required")
        if(len(token)<=1):
            return _("Header token filed is required")

        return "valid"

def isUserAuth(request):

    if request.user is not None and request.user.id != None:
        if request.user.isActive==False:
            return _("Your account inactive by administrator. please contact administrator")
        return True
    return True
    
def required_header_validate(headerData):

        if "language" not in headerData:
            return _("Language filed is required")

        translation.activate(headerData["language"])
        
        if "nonce" not in headerData:
            return _("Header nounce filed is required")

        if "timestamp" not in headerData:
            return _("Header timestamp filed is required")

        if "token" not in headerData:
            return _("Header token filed is required")

        nonce = headerData['nonce']
        timestamp = headerData['timestamp']
        token = headerData['token']
        secretKey = "w558XFrKN5Ue78eaLRsXSpe5zF9Q2jvC2b9DMM5r"
        privateKey = b"Hg1dhgKS1A1MT0AI5Pf5ydf7r6vlwgjUfa9s"

        secret_key = b"NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j"
        total_params = bytearray("nonce="+nonce+"&timestamp="+timestamp+"|"+secretKey,'utf-8')
        signature = hmac.new(privateKey, total_params, hashlib.sha256).hexdigest()

        if signature == token:
            return "valid"
        else:
            return _("Invalid Token")

def send_push_notification(body):

        serverToken = 'AAAAk1ZKv8s:APA91bGPYjlsXpljbzZNsixN1Rk53LFsVuwwE4HvHPaLeD3J9LvK8EafLR6vn1UaGKQABCACv5vZTly4nV9EEbdGHPZIhK0fAzYiNVBmx_YZOkKS3vV3axrYtW5Q915pbMVFB6tNiJ35'
   
        headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'key=' + serverToken,
                }
        
        response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
        return response.status_code
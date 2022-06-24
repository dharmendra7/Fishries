from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:

        data = list(response.data.values())[0]

        custom_response_data = { 
            'responseCode': response.status_code, # custom exception message
            'responseMessage': str((data)),
            # 'responseData':[]
        }
        response.data = custom_response_data
        response.status_code = 200
        # response.data['responseCode'] = response.status_code
        # response.data['responseMessage'] = response

    return response

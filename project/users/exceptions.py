from rest_framework.exceptions import APIException
from rest_framework import status


class BaseApiException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    err_message = 'Exception Occurred',
    err_title = 'Exception Occurred'
    err_dev_message = err_message

    def construct_detail(self):
        self.default_detail = {
            'err_message': self.err_message,
            'err_title': self.err_title,
            'err_dev_message': self.err_dev_message,
        }

    def __init__(self, *args, **kwargs):
        self.construct_detail()
        super().__init__(*args, **kwargs)


class InvalidPhoneNumberException(BaseApiException):
    err_message = 'Phone number is Invalid'
    err_title = 'Invalid Phone number.'


class InvalidOTPException(BaseApiException):
    err_message = 'OTP is Invalid or expired. Please Check and try again'
    err_title = 'Invalid OTP.'


class InvalidUserException(BaseApiException):

    def __init__(self, phone_no, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.err_message = f'User with phone number {phone_no} does not exist. Sign in first.'

    err_title = 'Invalid phone number'


class InvalidUsernameException(BaseApiException):
    err_message = 'Username is required when signing up.'
    err_title = 'Missing Details.'

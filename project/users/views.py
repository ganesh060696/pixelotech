import phonenumbers
from django.core.cache import cache

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

from project.json_rederer import ApiV3JSONRenderer
from .models import User
from .constants import OTP_KEY_FORMAT, OTP_KEY_TTL, STATIC_OTP
from .exceptions import InvalidPhoneNumberException, InvalidOTPException
from .serializers import UserSerializer
from .utils import UserUtils


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for User's to Log in, SignUp, Update details, Fetch Details and Delete Account
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    renderer_classes = [ApiV3JSONRenderer]

    def get_permissions(self):
        if self.action in ['generate_otp', 'verify_otp']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["POST"])
    def generate_otp(self, request, *args, **kwargs):
        """
        API to generate OTP and cache it with the Phone Number given
        """
        # Validate phone number and raise exception if it's not valid
        phone_number = UserUtils.strip_phone_number(request.data.get("phone_number"))
        phone_validation = phonenumbers.is_valid_number(phonenumbers.parse(phone_number))

        if not phone_validation:
            raise InvalidPhoneNumberException()

        # Cache OTP for the given Phone number and set TTL for the key
        cache.set(OTP_KEY_FORMAT.format(phone_number), STATIC_OTP, OTP_KEY_TTL)
        return Response({"message": "OTP Sent Successfully", "phone_number": phone_number})

    @action(detail=False, methods=["POST"])
    def verify_otp(self, request, *args, **kwargs):
        """
        API to Verify OTP received by user sent to the Phone Number,
        This API Verifies and creates User if Phone number does not exist in DB
        If phone number exists in DB, allows the user to log in to user account.
        """
        request_body = request.data
        phone_number = UserUtils.strip_phone_number(request_body['phone_number'])
        otp_received = request_body.get('otp_received', None)

        if otp_received is None:
            raise InvalidOTPException()

        # Checking if the OTP received is cached and not expired
        # If OTP matches with the Cached OTP, we allow the user to login or signup
        cached_otp = cache.get(OTP_KEY_FORMAT.format(phone_number))
        if cached_otp and str(otp_received) == str(cached_otp):
            cache.delete(OTP_KEY_FORMAT.format(phone_number))
            cache.set(OTP_KEY_FORMAT.format(phone_number), STATIC_OTP, OTP_KEY_TTL)

            # checking if user already Exists for the given mobile Number
            user = User.fetch_user_with_phone_number(phone_no=phone_number)
            if user is None:
                # Create a user if Phone number does not exist in DB
                user = User.objects.create_user(username=phone_number, hashed_phone_number=phone_number)
                message = "OTP Verified Successfully"
            else:
                message = f"Welcome {user.username}"

            return Response({"display_message": message,
                             "phone_number": phone_number,
                             "user": self.get_serializer(user).data})

        raise InvalidOTPException()

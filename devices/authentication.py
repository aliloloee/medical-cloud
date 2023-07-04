from rest_framework import HTTP_HEADER_ENCODING
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from devices.models import Device


DEVICE_HEADER_TYPE_BYTES = {h.encode(HTTP_HEADER_ENCODING) for h in settings.DEVICE_HEADER_TYPES}

class DeviceAuthentication() :

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.protocols = ['http', 'ws', ]
        self.device_model = Device

    def authenticate(self, request=None, protocol='http'):
        if protocol not in self.protocols :
            raise Exception(_('Wrong protocol!'))

        header = self.get_header(request, protocol)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        return self.validate_and_get_device_pk(raw_token)

    def get_header(self, request, protocol):
        """
        Extracts the header containing the device api_key from the given
        request.
        """
        if protocol == 'http' :
            header = request.META.get(settings.DEVICE_HEADER_NAME)
        elif protocol == 'ws' :
            header = dict(request['headers'])[settings.DEVICE_HEADER_NAME_WS.encode('utf-8')].decode('utf-8')


        # if isinstance(header, str):
        #     # Work around django test client oddness
        #     header = header.encode(HTTP_HEADER_ENCODING)

        return header

    def get_raw_token(self, header):
        """
        Extracts an unvalidated api_key from the given "Authorization"
        header value.
        """
        parts = header.split()

        if len(parts) == 0:
            return None

        if parts[0].encode('utf-8') not in DEVICE_HEADER_TYPE_BYTES:
            return None

        if len(parts) != 2:
            raise AuthenticationFailed(
                _("Authorization header must contain two space-delimited values"),
                code="bad_authorization_header",
            )

        return parts[1]

    def validate_and_get_device_pk(self, api_key):
        """
        Attempts to find and return a user using the given api_key.
        """

        try:
            device = Device.objects.get(api_key=api_key)
            user = device.user
        except self.device_model.DoesNotExist:
            raise AuthenticationFailed(_("Device not found"), code="user_not_found")

        if not device.is_active :
            raise AuthenticationFailed(_("Device is inactive"), code="user_inactive")

        # Shouldn't happen
        if not user.is_active:
            raise AuthenticationFailed(_("User is inactive"), code="user_inactive")

        return device


device_authenticator = DeviceAuthentication()
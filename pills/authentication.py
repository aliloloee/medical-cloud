from rest_framework import HTTP_HEADER_ENCODING
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from pills.models import PillAlarm



class PillAuthentication() :

    def __init__(self, *args, **kwargs):
        self.model = PillAlarm

    def authenticate(self, request=None):

        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        return self.validate_and_get_device_pk(raw_token)

    def get_header(self, request):
        """
        Extracts the header containing the device api_key from the given
        request.
        """
        header = dict(request['headers'])['alarm'.encode('utf-8')].decode('utf-8')

        return header

    def get_raw_token(self, header):
        """
        Extracts an unvalidated api_key from the given "Authorization"
        header value.
        """
        parts = header.split()

        if len(parts) == 0:
            return None

        if parts[0] not in ['Avian', ]:
            return None

        if len(parts) != 2:
            raise AuthenticationFailed(
                _("Authorization header must contain two space-delimited values"),
                code="bad_authorization_header",
            )
        
        return parts[1]

    def validate_and_get_device_pk(self, pk):
        """
        Attempts to find and return a user using the given api_key.
        """
        try:
            pill_alarm = self.model.objects.get(id=pk)
            user = pill_alarm.user
        except self.model.DoesNotExist:
            raise AuthenticationFailed(_("Alarm not found"), code="user_not_found")

        if not pill_alarm.is_active :
            raise AuthenticationFailed(_("Alarm is inactive"), code="user_inactive")

        # Shouldn't happen
        if not user.is_active:
            raise AuthenticationFailed(_("User is inactive"), code="user_inactive")

        return pill_alarm


pill_authenticator = PillAuthentication()
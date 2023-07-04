from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import APIException
from rest_framework import status
import six


class CustomValidation(APIException):
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('A server error occurred.')

    def __init__(self, detail=None, status_code=None):
        self.status_code = self.default_status_code if status_code is None else status_code
        self.detail = self.default_detail if detail is None else detail


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


class PasswordForgetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active) + six.text_type(user.updated) + six.text_type(user.last_login)
        )


def validate_password(password) :
    if settings.DEBUG :
        return
    for validator in settings.AUTH_PASSWORD_VALIDATORS_LIST :
        validator().validate(password)


account_activation_token = AccountActivationTokenGenerator()
account_reset_token = PasswordForgetTokenGenerator()


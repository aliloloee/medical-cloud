from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import filters
from random import choice, randrange, randint
from string import ascii_uppercase
import hashlib

DAKS = settings.DEVICE_API_KEY_SETTINGS

#? Might need some changes because it can produce same api_key
def generate_api_key():
    n = randrange(DAKS['MESSAGE_LOWER_BAND'], DAKS['MESSAGE_UPPER_BAND'])
    message = (''.join(choice(ascii_uppercase) for i in range(n))).encode()

    if DAKS['HASHING_METHOD'] == 'sha3_256' :
        api_key = hashlib.sha3_256(message).hexdigest()
    else : # default mode
        api_key = make_password(message)

    return api_key


def generate_otp():
    return str(randint( pow(10,settings.DEV_CODE_LENGTH-1) , pow(10, settings.DEV_CODE_LENGTH)-1 ))


class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user=request.user)


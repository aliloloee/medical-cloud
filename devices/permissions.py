from email import message
from re import T
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from django.conf import settings
from profiles.models import Profile
from devices.models import Device

class HasMinimumCharge(permissions.BasePermission) :
    """Allow users with minimum charge to request to the url."""
    message = "Inadequate charge for creating new device"

    def has_permission(self, request, view):

        profile = get_object_or_404(Profile, user=request.user)

        # FREE TYPE
        type = profile.type_in_string()
        if settings.MAX_NOD[type] == -1 :
            return True

        if profile.charge >= settings.MINIMUM_CHARGE_FOR_CREATE_NEW_DEVICE :
            return True

        return False


class CanStillCreateDevice(permissions.BasePermission) :
    """Allow users to create specific numbers of devices according to their profile type."""
    message = "Upgrade your profile to pro or advanced to be able to create more devices"

    def has_permission(self, request, view):

        user = request.user
        type = user.profile.type_in_string()

        # FREE TYPE
        if settings.MAX_NOD[type] == -1 :
            return True

        # OTHER TYPES
        device_count = Device.objects.filter(user=user).count()
        if device_count < settings.MAX_NOD[type] :
            return True

        return False


class DeviceIsValid(permissions.BasePermission) :
    """Allow owners to perform the actions on inactive devices"""

    def has_object_permission(self, request, view, obj):
        if (obj.user == request.user) and (obj.is_active == False) :
            return True

        return False


class DeviceIsActive(permissions.BasePermission) :
    """Allow owners to perform the actions only on active devices"""

    def has_object_permission(self, request, view, obj):
        if (obj.user == request.user) and (obj.is_active == True) :
            return True

        return False


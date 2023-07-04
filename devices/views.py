from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import get_language
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from devices import permissions, serializers
from devices.tasks import send_email_device
from devices.docs import schemas
from devices.models import Device
from devices import utils
from hub.redis_conf import HUBCACHE
from accounts.utils import CustomValidation


class ActivateDeviceAPI(generics.GenericAPIView):

    permission_classes = (IsAuthenticated, permissions.DeviceIsValid, )
    serializer_class = serializers.ActivateDeviceSerializer

    @swagger_auto_schema(**schemas['ActivateDeviceAPISchema']['PATCH'])
    def patch(self, request, device_id) :
        serializer = self.serializer_class(
                            self.get_object(),
                            context={'device_id' : device_id},
                            data=request.data
                            )

        if serializer.is_valid(raise_exception=True) :
            serializer.save()

            return Response(
                _('Device activated'),
                status = status.HTTP_200_OK
            )

    @swagger_auto_schema(**schemas['ActivateDeviceAPISchema']['GET'])
    def get(self, request, device_id) :
        instance = self.get_object()

        if HUBCACHE.check_key_existance(device_id) :
            return Response(
                _('Activation code is already sent.'),
                status = status.HTTP_208_ALREADY_REPORTED
            )

        send_email_device.apply_async(kwargs={
                                    'device_id': device_id, 
                                    'lang': get_language(),
                                    'to':instance.user.email
                                    })

        return Response(
            data={
                'device_id': device_id,
                'expiration_time_seconds': settings.DEVICE_ACTIVATION_CODE_EXPIRATION_TIMESTAMP
            },
            status = status.HTTP_201_CREATED
            )

    def get_object(self):
        try :
            obj = Device.inactive_objects.get(pk=self.kwargs['device_id'])
        except :
            raise CustomValidation(
                _('Object Not Valid!'),
                status_code=status.HTTP_404_NOT_FOUND
            )
        return obj


class DeviceViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet) :

    queryset = Device.objects.all()
    serializer_class = serializers.DeviceSerializer
    filter_backends = (utils.IsOwnerFilterBackend, )
    
    #* Put and Patch are always added together because both are within mixins.UpdateModelMixin
    #* We can keep one of them using http_method_names
    http_method_names = ['get', 'post', 'put']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = (IsAuthenticated, )
        else:
            permission_classes = (
                                    IsAuthenticated, 
                                    permissions.HasMinimumCharge,
                                    permissions.CanStillCreateDevice
                                ) 
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(**schemas['DeviceAPISchema']['CREATE'])
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        if response.status_code == 201 :
            response.data['expiration_time_seconds'] = settings.DEVICE_ACTIVATION_CODE_EXPIRATION_TIMESTAMP

            device_id = response.data['id']
            try :
                to = Device.objects.get(pk=device_id).user.email
            except :
                raise CustomValidation(
                    _('Object Not Valid!'),
                    status_code=status.HTTP_404_NOT_FOUND
                )

            send_email_device.apply_async(kwargs={
                                    'device_id': device_id, 
                                    'lang': get_language(),
                                    'to': to
                                    })

        return response

    @swagger_auto_schema(**schemas['DeviceAPISchema']['LIST'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(**schemas['DeviceAPISchema']['RETRIEVE'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(**schemas['DeviceAPISchema']['UPDATE'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class OverrideAPIKey(mixins.UpdateModelMixin,
                    generics.GenericAPIView) :

    permission_classes = (IsAuthenticated, permissions.DeviceIsActive, )
    serializer_class = serializers.OverrideDeviceAPIKey

    @swagger_auto_schema(**schemas['OverrideAPIKeySchema'])
    def patch(self, request, device_id) :
        serializer = self.serializer_class(
                            self.get_object(),
                            context={'device_id' : device_id},
                            data=request.data
                            )

        if serializer.is_valid(raise_exception=True) :
            data = serializer.save()

            return Response(
                _('Device api key successfully overrided.'),
                data,
                status = status.HTTP_200_OK
            )

    def get_object(self):
        try :
            obj = Device.active_objects.get(pk=self.kwargs['device_id'])
        except :
            raise CustomValidation(
                _('Object Not Valid!'),
                status_code=status.HTTP_404_NOT_FOUND
            )
        return obj


class DeviceLatestRecordAPI(generics.GenericAPIView) :

    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.LastRecordsSerializer

    @swagger_auto_schema(**schemas['DeviceLatestRecordAPISchema'])
    def get(self, request):

        user = request.user
        serializer = self.serializer_class(user)

        return Response(
            serializer.data,
            status = status.HTTP_200_OK,
        )






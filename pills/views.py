from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _

from pills.models import UniversalPill, Pill, PillAlarm, AlarmNotification
from pills import serializers
from pills.utils import IsOwnerFilterBackend
from pills.docs import schemas

from drf_yasg.utils import swagger_auto_schema




class UniversalPillModelViewSet(mixins.ListModelMixin, viewsets.GenericViewSet) :
    """
    This view provides the possibility of listing all the pills which have beed added to db by the admin.

    The access for staff and normal users are different. While staff who request to this view have access to all the pill, active or inactive, with all the details of every pill, normal users have only access to active pill and in case of details only name, description and application of such pills.

    * To extend this view, for other actions such as "create", "retrieve", "update", "patch" and "destroy", simply the view needs to heritate from viewsets.ModelViewSet and other methods need to be uncommented as well

    * In order to change access level and fields which are accessable for users, these three methods need to be modified : "get_permissions", "get_serializer_class" and "get_queryset".
    """

    model = UniversalPill
    # http_method_names = ['get', 'post', 'put', 'delete']

    def get_permissions(self):
        user = self.request.user
        if self.action == 'list' and not(user.is_staff):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self, *args, **kwargs):
        user = self.request.user
        if self.action == 'list' and not(user.is_staff):
            serializer_classes = serializers.UniversalPillClientSerializer
        else:
            serializer_classes = serializers.UniversalPillAdminSerializer
        return serializer_classes
    
    def get_queryset(self):
        user = self.request.user
        if self.action == 'list' and not(user.is_staff):
            return UniversalPill.active_objects.all()
        else :
            return UniversalPill.objects.all()
        
    # @swagger_auto_schema(**schemas['UniversalPillModelViewSetSchema']['CREATE'])
    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)
        
    @swagger_auto_schema(**schemas['UniversalPillModelViewSetSchema']['LIST'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    # @swagger_auto_schema(**schemas['UniversalPillModelViewSetSchema']['RETRIEVE'])
    # def retrieve(self, request, *args, **kwargs):
    #     return super().retrieve(request, *args, **kwargs)
    
    # @swagger_auto_schema(**schemas['UniversalPillModelViewSetSchema']['UPDATE'])
    # def update(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)
    
    # @swagger_auto_schema(**schemas['UniversalPillModelViewSetSchema']['DESTROY'])
    # def destroy(self, request, *args, **kwargs):
    #     return super().destroy(request, *args, **kwargs)


class UniversalPillLookUpAPIView(generics.GenericAPIView) :
    """
    This view provides the possibility of listing the pill names via a keyword argument which is recieved by this view. This view is for quick searching funcionalities where usere are trying to find some pill by typing the first letters of those pills.

    * To extend the retrieved fields, the query which is made to the db must be modified as well as the serializer fields.
    
    * In order to make this view more efficient, serializer.data needs to cached. On the other hand, this cached data needs to be deleted every time a new UniversalPill is added to the db. This is easily achievable through the save method of this model or even through the signal.
    """

    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.UniversalPillSearchLookUPSerializer

    @swagger_auto_schema(**schemas['UniversalPillLookUpSchema'])
    def get(self, request, keyword) :
        pill_names = UniversalPill.active_objects.filter(name__startswith=keyword).only('name')
        serializer = self.serializer_class(pill_names, many=True)

        return Response(
                serializer.data,
                status = status.HTTP_200_OK
            )


class PillModelViewSet(
                        mixins.UpdateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.GenericViewSet
                        ) :
    """
    This view provides the possibility of listing, modifying and updating all the pills which have beed added to db by the normal users.

    * To extend this view for "destroy" action, it would be better not to have a CASCADE deleting strategy for the related model. We don't want to lose any data of any user since these data might be valuable for future AI purposes. So, We need to somehow archive these data:
        1- As a way of example, we can add a "is_deleted" field to the Pill model which is False by default. When a user deletes a pill, this field is set to True (user can't change this field to False). We also need a suitable manager in Pill model as well. Also, the other models which have a foreignKey to Pill model need to be archived as well.
    """

    queryset = Pill.objects.all()
    serializer_class = serializers.PillSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = [IsOwnerFilterBackend, ]
    http_method_names = ['get', 'post', 'put',]

    @swagger_auto_schema(**schemas['PillModelViewSetSchema']['CREATE'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
        
    @swagger_auto_schema(**schemas['PillModelViewSetSchema']['LIST'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(**schemas['PillModelViewSetSchema']['RETRIEVE'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(**schemas['PillModelViewSetSchema']['UPDATE'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    # @swagger_auto_schema(**schemas['UniversalPillModelViewSetSchema']['DESTROY'])
    # def destroy(self, request, *args, **kwargs):
    #     return super().destroy(request, *args, **kwargs)


class PillAlarmViewSet(
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet
                        ) :
    """
    This view provides the possibility of listing, creating alarms for each pill that was added before by the user.

    * To extend this view for "destroy" action, it would be better to not have a CASCADE deleting strategy for the related model. We don't want to lose any data of any user since these data might be valuable for future AI purposes. So, We need to somehow archive these data.
    """
    
    queryset = PillAlarm.objects.all()
    permission_classes = [IsAuthenticated, ]
    filter_backends = [IsOwnerFilterBackend]
    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'patch']

    def get_serializer_class(self):
        if self.action == 'update' :
            return serializers.PillAlarmUpdateSerializer
        else :
            return serializers.PillAlarmSerializer
        
    @swagger_auto_schema(**schemas['PillAlarmViewSetSchema']['UPDATE'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(**schemas['PillAlarmViewSetSchema']['RETRIEVE'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(**schemas['PillAlarmViewSetSchema']['LIST'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(**schemas['PillAlarmViewSetSchema']['CREATE'])
    def create(self, request, *args, **kwargs):
        user = request.user

        self.serializer_class = self.get_serializer_class()

        serializer = self.serializer_class(
                            context={'user': user},
                            data=request.data
                            )
        
        if serializer.is_valid() :
            try :
                alarm = serializer.save()
            except IntegrityError :
                return Response(
                    _('Each pill can have only one alarm. If thats not the case then there is an internal error!'),
                    status = status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(
            serializer.data,
            status = status.HTTP_201_CREATED
        )


class AlarmNotificationViewSet(
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet
                        ) :
    
    """
    This view provides the possibility of listing, creating and updating alarm notifications for each alarm that was added before by the user.

    * The "destroy" action not implemented
    """
    
    queryset = AlarmNotification.objects.all()
    permission_classes = [IsAuthenticated, ]
    filter_backends = [IsOwnerFilterBackend]
    lookup_field = 'pk'
    http_method_names = ['get', 'post', 'patch', ]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update', ] :
            return serializers.AlarmNotificationUpdateSerializer
        else :
            return serializers.AlarmNotificationSerializer

    @swagger_auto_schema(**schemas['AlarmNotificationViewSetSchema']['PARTIAl_UPDATE'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(**schemas['AlarmNotificationViewSetSchema']['RETRIEVE'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(**schemas['AlarmNotificationViewSetSchema']['LIST'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(**schemas['AlarmNotificationViewSetSchema']['CREATE'])
    def create(self, request, *args, **kwargs):
        user = request.user

        self.serializer_class = self.get_serializer_class()

        serializer = self.serializer_class(
                            context={'user': user},
                            data=request.data
                            )
        
        if serializer.is_valid() :
            notification = serializer.save()

        return Response(
            serializer.data,
            status = status.HTTP_201_CREATED
        )


class PillAlarmActivationAPIView(generics.GenericAPIView) :
    """
    This view provides the possibility of setting interval for alarm notification. The notifications are recieved through related websocket routings.

    * The delete method does not delete the alarm but instead clears the interval from the alarm.
    """

    queryset = PillAlarm.objects.all()
    serializer_class = serializers.PillAlarmPeriodicTaskCreationSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = [IsOwnerFilterBackend, ]
    lookup_field = 'pk'

    @swagger_auto_schema(**schemas['PillAlarmActivationAPIView']['UPDATE'])
    def patch(self, requset, pk) :
        alarm = self.get_object()

        serializer = self.serializer_class(alarm, data=requset.data, partial=True)
        if serializer.is_valid(raise_exception=True) :
            serializer.save()

        return Response(
            _('Interval added to alarm'),
            status=status.HTTP_201_CREATED
        )

    @swagger_auto_schema(**schemas['PillAlarmActivationAPIView']['DELETE'])
    def delete(self, request, pk) :
        alarm = self.get_object()

        if alarm.periodic_task != None :
            alarm.periodic_task.enabled = False
            alarm.periodic_task.delete()

        return Response(
            _('Interval removed from alarm'),
            status=status.HTTP_200_OK
        )

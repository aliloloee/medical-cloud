from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from django.utils.translation import gettext_lazy as _

from checkup.models import BloodTest, BloodTestResult
from checkup import serializers
from checkup.utils import IsOwnerFilterBackend, check_up_categorical_values
from checkup.docs import schemas

from drf_yasg.utils import swagger_auto_schema



class BloodTestViewSet(
                        mixins.UpdateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet
                        ) :

    queryset = BloodTest.objects.all()
    serializer_class = serializers.BloodTestSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = [IsOwnerFilterBackend, ]
    lookup_field = 'pk'
    # http_method_names = ['get', 'post', 'put', 'delete']

    @swagger_auto_schema(**schemas['BloodTestViewSetSchema']['CREATE'])
    def create(self, request, *args, **kwargs):
        user = request.user

        self.serializer_class = self.get_serializer_class()

        serializer = self.serializer_class(
                            context={'user': user},
                            data=request.data
                            )
        
        if serializer.is_valid() :
            try :
                blood_test = serializer.save()
            except :
                return Response(
                    _('Bad request'),
                    status = status.HTTP_400_BAD_REQUEST
                )

        return Response(
            serializer.data,
            status = status.HTTP_201_CREATED
        )
        
    @swagger_auto_schema(**schemas['BloodTestViewSetSchema']['LIST'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(**schemas['BloodTestViewSetSchema']['RETRIEVE'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(**schemas['BloodTestViewSetSchema']['UPDATE'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(**schemas['BloodTestViewSetSchema']['DESTROY'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class BloodTestResultsViewSet(
                        mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet
                        ) :

    queryset = BloodTestResult.objects.all()
    serializer_class = serializers.BloodTestResultSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = [IsOwnerFilterBackend, ]
    lookup_field = 'pk'

    @swagger_auto_schema(**schemas['BloodTestResultsViewSetSchema']['CREATE'])
    def create(self, request, *args, **kwargs):
        user = request.user

        self.serializer_class = self.get_serializer_class()

        serializer = self.serializer_class(
                            context={'request': request},
                            data=request.data
                            )
        
        if serializer.is_valid() :
            try :
                blood_test = serializer.save()
            except :
                return Response(
                    _('Bad request'),
                    status = status.HTTP_400_BAD_REQUEST
                )

        return Response(
            serializer.data,
            status = status.HTTP_201_CREATED
        )

    @swagger_auto_schema(**schemas['BloodTestResultsViewSetSchema']['RETRIEVE'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(**schemas['BloodTestResultsViewSetSchema']['UPDATE'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(**schemas['BloodTestResultsViewSetSchema']['DESTROY'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class BloodTestDetailsViewSet(
                        mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.GenericViewSet
                        ) :

    queryset = BloodTest.objects.all()
    permission_classes = [IsAuthenticated, ]
    serializer_class = serializers.BloodTestDetailsSerializer
    filter_backends = [IsOwnerFilterBackend, ]
    lookup_field = 'pk'

    @swagger_auto_schema(**schemas['BloodTestDetailsViewSetSchema']['RETRIEVE'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(**schemas['BloodTestDetailsViewSetSchema']['CREATE'])
    def create(self, request, *args, **kwargs):
        self.serializer_class = self.get_serializer_class()

        serializer = self.serializer_class(
                            context={'request': request},
                            data=request.data
                            )
        
        if serializer.is_valid() :
            try :
                blood_test = serializer.save()
            except :
                return Response(
                    _('Bad request'),
                    status = status.HTTP_400_BAD_REQUEST
                )

        return Response(
            serializer.data,
            status = status.HTTP_201_CREATED
        )


class CheckUpCategoricalValuesAPI(generics.RetrieveAPIView) :

    @swagger_auto_schema(**schemas['CheckUpCategoricalValuesAPISchema'])
    def get(self, request):
        response = check_up_categorical_values()

        return Response(
            response,
            status=status.HTTP_200_OK
            )
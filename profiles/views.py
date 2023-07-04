from rest_framework import generics, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from profiles import serializers
from profiles.models import Profile, CustomProfile
from profiles.docs import schemas
from profiles.utils import custom_profile_categorical_values 



class ProfileAPI(generics.RetrieveAPIView) :

    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.ProfileSerializer

    @swagger_auto_schema(**schemas['ProfileAPISchema'])
    def get(self, request):
        try :
            profile = request.user.profile
        except :
            return Response(
                _("Profile is faulty!!"),
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(profile)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
            )


class ProfileChargeAPI(mixins.UpdateModelMixin, generics.GenericAPIView) :

    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.ProfileSerializer

    @swagger_auto_schema(**schemas['ProfileChargeAPISchema'])
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get_object(self):
        # obj = Profile.objects.get(user=self.request.user)
        obj = get_object_or_404(Profile, user=self.request.user)
        return obj


class CustomProfileAPI(generics.RetrieveAPIView) :

    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.CustomProfileSerializer

    @swagger_auto_schema(**schemas['CustomProfileAPISchema'])
    def get(self, request):
        try :
            profile = request.user.custom_profile
        except :
            return Response(
                _("Profile is faulty!!"),
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(profile)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
            )


class CustomProfileUpdateAPI(mixins.UpdateModelMixin, generics.GenericAPIView) :

    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.CustomProfileSerializer

    @swagger_auto_schema(**schemas['CustomProfileUpdateAPISchema'])
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get_object(self):
        obj = get_object_or_404(CustomProfile, user=self.request.user)
        return obj


class CustomProfileCategoricalValuesAPI(generics.RetrieveAPIView) :

    @swagger_auto_schema(**schemas['CustomProfileCategoricalValuesAPISchema'])
    def get(self, request):
        response = custom_profile_categorical_values()

        return Response(
            response,
            status=status.HTTP_200_OK
            )



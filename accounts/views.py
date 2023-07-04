from django.utils.translation import get_language
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.utils import swagger_auto_schema
from accounts.utils import (account_activation_token as aat, account_reset_token as art)
from accounts import serializers
from accounts.permissions import AnyOnPost_AuthOnGet
from accounts.tasks import send_email
from accounts.docs import schemas
import uuid


class RegisterAPIView(generics.CreateAPIView) :

    serializer_class = serializers.RegisterUserSerializer
    permission_classes = (AnyOnPost_AuthOnGet, )

    @swagger_auto_schema(**schemas['RegisterAPISchema'])
    def post(self, request) :

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid() :
            user = serializer.save()

            send_email.apply_async(kwargs={
                                'token': aat.make_token(user),
                                'hub_id': str(user.hub_id),
                                'lang': get_language(),
                                'to': user.email,
                                'activation': True 
                                })

            return Response(
                serializer.data,
                status = status.HTTP_201_CREATED
            )
        else :
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST,
            )

    @swagger_auto_schema(**schemas['UserAPIViewSchema'])
    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
            )


class VerifyAPIView(generics.GenericAPIView) :

    serializer_class = serializers.VerifyUserSerializer

    @swagger_auto_schema(**schemas['VerifyAPISchema'])
    def post(self, request, token, hub_id):
        
        try :
            uid = uuid.UUID(hub_id)
            user = get_user_model().objects.get(hub_id=uid)
        except :
            user = None

        if user is not None and aat.check_token(user, token):
            serializer = self.serializer_class(user)
            return Response(
                serializer.data,
                status = status.HTTP_200_OK,
            )
        else:
            return Response(
                status = status.HTTP_400_BAD_REQUEST,
            )


class PasswordChangeAPIView(generics.GenericAPIView) :

    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.PasswordChangeSerializer

    @swagger_auto_schema(**schemas['PasswordChangeAPISchema'])
    def patch(self, request) :
        serializer = self.serializer_class(context = {'request':request}, data=request.data)

        if serializer.is_valid() :
            serializer.save()
            
            return Response(
                status = status.HTTP_200_OK
            )
        else :
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST,
            )


class ForgetPasswordAPIView(generics.GenericAPIView) :

    serializer_class = serializers.ForgetPasswordSerializer

    @swagger_auto_schema(**schemas['ForgetPasswordAPISchema'])
    def post(self, request) :

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid() :
            user = serializer.save()

            send_email.apply_async(kwargs={
                                'token': art.make_token(user),
                                'hub_id': str(user.hub_id),
                                'lang': get_language(),
                                'to': user.email,
                                'reset': True
                                })

            return Response(
                    status = status.HTTP_200_OK
                )
        else :
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
                )


class ResetPasswordAPIView(generics.GenericAPIView) :

    serializer_class = serializers.ResetPasswordSerializer

    @swagger_auto_schema(**schemas['ResetPasswordAPISchema'])
    def post(self, request, token, hub_id) :

        try :
            uid = uuid.UUID(hub_id)
            user = get_user_model().objects.get(hub_id=uid)
        except :
            user = None

        if user is None :
            return Response(status = status.HTTP_400_BAD_REQUEST)

        if not art.check_token(user, token) :
            return Response(
                status = status.HTTP_400_BAD_REQUEST,
            )
    
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid() :
            serializer.save(user)
            return Response(status = status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):

    @swagger_auto_schema(**schemas['CustomTokenObtainPairSchema'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenRefreshView(TokenRefreshView):
    
    @swagger_auto_schema(**schemas['CustomTokenRefreshViewSchema'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LogoutAPIView(generics.GenericAPIView) :

    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.LogoutAPISerializer

    @swagger_auto_schema(**schemas['LogoutAPIViewSchema'])
    def post(self, request) :
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True) :
            return Response(
                "Successful Logout",
                status = status.HTTP_200_OK
                )




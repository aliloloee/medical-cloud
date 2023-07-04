from rest_framework import serializers, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model 
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from accounts.utils import validate_password, CustomValidation
from profiles.tasks import send_email_custom_profile



User = get_user_model()

class RegisterUserSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        ref_name = None # This property helped documenting nested-serializer of url "profiles:api-profile-charge"
        model = User
        fields = ('id', 'email', 'firstname', 'lastname', 'password', 'confirm_password', )

        extra_kwargs = {
            'password': {
                'write_only' : True,
                'style' : {'input_type' : 'password'},
            },
            'confirm_password': {
                'write_only' : True,
                'style' : {'input_type' : 'password'},
            }
        }

    def validate(self, data) :
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(_("Passwords do not match"))
        validate_password(data['password'])
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        return User.objects.create_user(**validated_data)


class VerifyUserSerializer(serializers.BaseSerializer) :

    class Meta:
        ref_name = None

    def to_representation(self, instance):
        instance.is_active = True
        instance.save()
        send_email_custom_profile.apply_async(kwargs={
                                        'lang': get_language(),
                                        'to': instance.email,
                                        'firstname': instance.firstname,
                                        'lastname': instance.lastname,
                                        })
        refresh = TokenObtainPairSerializer().get_token(instance)
        return {
            'refresh' : str(refresh),
            'access' : str(refresh.access_token)
        }


class PasswordChangeSerializer(serializers.Serializer):

    class Meta:
        ref_name = None

    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    new_password_repeat = serializers.CharField(required=True, write_only=True)

    def validate(self, data) :
        user = self.context['request'].user

        if user is None:
            raise serializers.ValidationError(_("Bad Request"))

        if not user.check_password(data['old_password']) :
            raise serializers.ValidationError(_("Bad Request"))

        if data['new_password'] != data['new_password_repeat']:
            raise serializers.ValidationError(_("Passwords do not match"))
        
        validate_password(data['new_password'])

        data['user'] = user
        return data

    def save(self) :
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.save()


class ForgetPasswordSerializer(serializers.Serializer) :

    class Meta:
        ref_name = None

    email = serializers.EmailField()

    def validate(self, data) :
        q = User.objects.filter(email=data['email'])

        # No existing user or user not varyfied
        if len(q) == 0 or (not q.first().is_active ) :
            raise serializers.ValidationError(_('Bad Request'))

        data['user'] = q.first()
        return data

    def save(self) :
        return self.validated_data['user']


class ResetPasswordSerializer(serializers.Serializer) :

    class Meta:
        ref_name = None

    new_password = serializers.CharField(required=True, write_only=True)
    new_password_repeat = serializers.CharField(required=True, write_only=True)

    def validate(self, data) :

        if data['new_password'] != data['new_password_repeat']:
            raise serializers.ValidationError(_("Passwords do not match"))
        
        validate_password(data['new_password'])

        return data

    def save(self, user) :
        user.set_password(self.validated_data['new_password'])
        user.save()


class LogoutAPISerializer(serializers.Serializer) :

    class Meta:
        ref_name = None
    
    refresh = serializers.CharField(write_only=True)

    def validate(self, data) :
        try :
            token = RefreshToken(data['refresh'])
            token.blacklist()
        except TokenError :
            raise CustomValidation(
                        _('Refresh token was not included in request data.'),
                        status_code=status.HTTP_401_UNAUTHORIZED
                        )
        return data


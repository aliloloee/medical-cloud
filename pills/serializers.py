from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from pills.models import UniversalPill, Pill, PillAlarm, AlarmNotification





class UniversalPillAdminSerializer(serializers.ModelSerializer) :
    """
    This serializer is written for staff users in which all fields of UniversalPill model instances are serialized.
    """
    class Meta :
        ref_name = None
        model = UniversalPill
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', )


class UniversalPillClientSerializer(serializers.ModelSerializer) :
    """
    This serializer is written for normal users in which only a few fields of UniversalPill model instances are serialized.
    """
    class Meta :
        ref_name = None
        model = UniversalPill
        fields = ('name', 'description', 'application', )


class UniversalPillSearchLookUPSerializer(serializers.ModelSerializer) :
    """
    This serializer is written for searching purposes in which the names of UniversalPill model instances are serialized.
    """
    class Meta :
        ref_name = None
        model = UniversalPill
        fields = ('name',)


class PillSerializer(serializers.ModelSerializer) :
    """
    This serializer is written for normal users in which only a few fields of Pill model instances are serialized.
    """
    class Meta :
        ref_name = None
        model = Pill
        fields = ('id', 'name', 'description', )

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        instance = super().create(validated_data)
        instance.save()
        return instance


class PillAlarmSerializer(serializers.ModelSerializer) :
    """
    This serializer is written for normal users in which all fields except the periodic task are serialized.

    * The pill id needs to be included for creating new alarms.
    * The "is_active" field is read_only in this serializer, because the activation process of an alarm is dependent on the periodic task of an alarm. Activation is written in another serializer class.
    """
    pill_id = serializers.UUIDField(write_only=True)

    class Meta :
        ref_name = None
        model = PillAlarm
        fields = ('id', 'description', 'is_active', 'pill_id')
        read_only_fields = ('id', 'is_active')

    def validate(self, data):
        pill_id = data['pill_id']
        user = self.context['user']
        try :
            self.pill = Pill.objects.get(pk=pill_id)
        except :
            raise serializers.ValidationError(
                            _('Object not valid.'),
                            )
        if self.pill.user != user :
            raise serializers.ValidationError(
                            _('Object not valid.'),
                            )
        return data

    def create(self, validated_data):
        user = self.context['user']
        validated_data['user'] = user
        validated_data['pill'] = self.pill
        instance = super().create(validated_data)
        instance.save()
        return instance


class PillAlarmUpdateSerializer(serializers.ModelSerializer) :
    """
    This serializer is specifically written for updating methods in the views where "pill_id" is no longer required. All fields except periodic task are serialized.
    """
    class Meta :
        ref_name = None
        model = PillAlarm
        fields = ('id', 'description', 'is_active',)
        read_only_fields = ('id', 'is_active')


class AlarmNotificationSerializer(serializers.ModelSerializer) :
    """
    This serializer is written for normal users in which all fields of AlarmNotification model are serialized.

    * The alarm id needs to be included for creating new notifications.
    """
    alarm_id = serializers.UUIDField(write_only=True)

    class Meta :
        ref_name = None
        model = AlarmNotification
        fields = ('id', 'consumed', 'consumed_at', 'alarm_id', )

    def validate(self, data):
        alarm_id = data['alarm_id']
        user = self.context['user']
        try :
            self.alarm = PillAlarm.objects.get(pk=alarm_id)
        except :
            raise serializers.ValidationError(
                            _('Object not valid.'),
                            )
        if self.alarm.user != user :
            raise serializers.ValidationError(
                            _('Object not valid.'),
                            )
        return data

    def create(self, validated_data):
        user = self.context['user']
        validated_data['user'] = user
        validated_data['alarm'] = self.alarm
        instance = super().create(validated_data)
        instance.save()
        return instance


class AlarmNotificationUpdateSerializer(serializers.ModelSerializer) :
    """
    This serializer is specifically written for updating methods in the views where "alarm_id" is no longer required.
    """
    class Meta :
        ref_name = None
        model = AlarmNotification
        fields = ('id', 'consumed', 'consumed_at', )
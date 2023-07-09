from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from django_celery_beat.models import IntervalSchedule, PeriodicTask

from pills.models import UniversalPill, Pill, PillAlarm, AlarmNotification

import json



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
    """
    pill_id = serializers.UUIDField(write_only=True)

    class Meta :
        ref_name = None
        model = PillAlarm
        fields = ('id', 'description', 'pill_id')
        read_only_fields = ('id',)

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
        fields = ('id', 'description',)
        read_only_fields = ('id',)


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


class PillAlarmPeriodicTaskCreationSerializer(serializers.Serializer) :
    """
    This serializer is written for creating periodic task and assign it to a existing alarm.

    * For now the periodic task is written based on interval, but it is better to modify this to a crontab periodic task since interval periodic task can malfunction if the server goes down for some reason.
    """

    seconds = serializers.IntegerField()

    class Meta :
        model = PillAlarm

    def validate(self, data):
        seconds = data['seconds']

        if seconds < settings.PILL_ALARM_MIN_INTERVAL :
            raise serializers.ValidationError(
                            _('Alarm interval is small!!'),
                            )
        return data

    def update(self, instance, validated_data):
        seconds = validated_data.get('seconds')

        schedule, created = IntervalSchedule.objects.get_or_create(
            every=seconds,
            period=IntervalSchedule.SECONDS,
        )

        name = f'send pill notification for alram-id of {instance.pk}'

        # In case the alarm has an active periodic task
        previous_task = instance.periodic_task
        if previous_task != None :
            instance.periodic_task.enabled = False
            instance.periodic_task.delete()

        periodic_task = PeriodicTask.objects.create(
                    interval=schedule,
                    name=name,
                    task='pills.tasks.send_pill_notification',
                    kwargs=json.dumps({
                        'pill': instance.pill.name,
                        'alarm-id' : str(instance.pk),
                        'user': instance.user.firstname
                    }),
                )

        instance.periodic_task = periodic_task
        instance.save()

        return instance


from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from devices.models import Device, Record
from devices.utils import generate_api_key
from hub.redis_conf import HUBCACHE


class DeviceSerializer(serializers.ModelSerializer) :

    class Meta :
        ref_name = None
        model = Device
        fields = ('id', 'api_key', 'name', 'description', 'serial_number', 'is_active', )
        read_only_fields = ('id', 'api_key', 'is_active', )

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.user = self.context['request'].user
        instance.save()
        return instance


class ActivateDeviceSerializer(serializers.Serializer) :

    class Meta:
        ref_name = None

    code = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        device_id = self.context['device_id']

        if not HUBCACHE.check_key_value_validity(key=device_id, value=data['code']) :
            raise serializers.ValidationError(
                            _('Activation code is either expired or wrong.'),
                            )

        return data

    def update(self, instance, validated_data):
        instance.is_active = True
        instance.save()
        HUBCACHE.delete_key(instance.pk)
        return {
            'device_id' : instance.pk
        }


class OverrideDeviceAPIKey(serializers.Serializer) :

    name = serializers.CharField()

    class Meta :
        ref_name = None

    def validate(self, data):
        if data['name'] != self.instance.name :
            raise serializers.ValidationError(_('Device name is wrong!'))

        return data

    def update(self, instance, validated_data):
        instance.api_key = generate_api_key()
        instance.save()
        return {
            'api_key' : instance.api_key
        }


class LastRecordsSerializer(serializers.BaseSerializer) :

    class Meta:
        ref_name = None

    def to_representation(self, instance):
        devs = Device.active_objects.filter(user=instance)
        response = dict()
        for dev in devs :
            r = Record.objects.filter(device=dev).last()
            response[dev.name] = (str(dev.id), r.data)

        return response


# from rest_framework.throttling import BaseThrottle
# class CreateDeviceSyncData(serializers.ModelField) :

#     class Meta :
#         ref_name = None
#         model = Data
#         fields = ('id', 'title', 'file', )


#     def validate(self, data) :
#         # Validate api_key
#         # Validate charge > 0
#         # validate file size
#         # validate max_number_of_requests < limit
#         pass




from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework.fields import empty

from checkup.models import BloodTest, BloodTestResult
from checkup import utils

from accounts.serializers import RegisterUserSerializer



class BloodTestSerializer(serializers.ModelSerializer) :

    def __init__(self, *args, **kwargs):
        self.gender_types = utils.GenderType.all_types()
        super().__init__(*args, **kwargs)

    class Meta :
        ref_name = None
        model = BloodTest
        exclude = ('created', 'updated', 'user', )
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = self.context['user']
        validated_data['user'] = user
        instance = super().create(validated_data)
        instance.save()
        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['gender'] = self.gender_types[ret['gender']]
        return ret


class BloodTestResultSerializer(serializers.ModelSerializer) :
    blood_test_id = serializers.UUIDField(write_only=True)

    class Meta :
        ref_name = None
        model = BloodTestResult
        fields = ('id', 'name', 'value', 'blood_test_id', )
        read_only_fields = ('id',)

    def validate(self, data):
        request = self.context['request']
        if request.method in ['POST', 'post'] :
            blood_test_id = data['blood_test_id']
            user = self.context['request'].user
            try :
                self.blood_test = BloodTest.objects.get(pk=blood_test_id)
            except :
                raise serializers.ValidationError(
                                _('Object not valid.'),
                                )
            if self.blood_test.user != user :
                raise serializers.ValidationError(
                                _('Object not valid.'),
                                )

        elif request.method in ['put', 'patch'] :
            try :
                blood_test_id = data['blood_test_id']
            except :
                blood_test_id = None
            user = self.context['request'].user
            if blood_test_id :
                try :
                    self.blood_test = BloodTest.objects.get(pk=blood_test_id)
                except :
                    raise serializers.ValidationError(
                                    _('Object not valid.'),
                                    )
                if self.blood_test.user != user :
                    raise serializers.ValidationError(
                                    _('Object not valid.'),
                                    )
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        validated_data['blood_test'] = self.blood_test
        instance = super().create(validated_data)
        instance.save()
        return instance


class BloodTestResultUpdateSerializer(serializers.ModelSerializer) :

    def __init__(self, *args, **kwargs):
        self.blood_test_all_types = utils.BloodTestArticles.all_types()
        super().__init__(*args, **kwargs)

    class Meta :
        ref_name = None
        model = BloodTestResult
        fields = ('id', 'name', 'value', )
        read_only_fields = ('id',)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['name'] = self.blood_test_all_types[ret['name']]
        return ret


class BloodTestDetailsSerializer(serializers.ModelSerializer) :

    def __init__(self, *args, **kwargs):
        self.gender_types = utils.GenderType.all_types()
        super().__init__(*args, **kwargs)

    blood_test_results = BloodTestResultUpdateSerializer(many=True)

    class Meta :
        ref_name = None
        model = BloodTest
        exclude = ('created', 'updated', 'user', )
        read_only_fields = ('id',)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['gender'] = self.gender_types[ret['gender']]
        return ret

    def create(self, validated_data):
        user = self.context['request'].user

        blood_test_results = validated_data.pop('blood_test_results')

        blood_test = BloodTest.objects.create(user=user, **validated_data)
        for blood_test_result in blood_test_results:
            BloodTestResult.objects.create(blood_test=blood_test, user=user, **blood_test_result)
        return blood_test


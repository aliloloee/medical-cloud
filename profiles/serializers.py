from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from profiles.models import Profile, CustomProfile
from profiles import utils
from accounts.serializers import RegisterUserSerializer

#* DRF_YASG seems to have problem documenting request-body of nested serializers, specifically, in our case
#* the fields related to user appear in request-body of swagger (not for get requests) while 'user' is set as
#* read-only.
#* In general, there are two solutions to this case:
#* 1- set many=True for child serializer in the parent serializer 
        # In our case : (user = RegisterUserSerializer(read_only=True, many=True)) 
        # However in our case this won't work because for each profile there's only one user not many
#* 2- set ref_name=None in Meta class of child serializer
        # The consequence of this approach is losing inline model schema in swagger

class ProfileSerializer(serializers.ModelSerializer) :
    """
    ProfileSerializer is for representation of the profile and the amount of charge.
    Changing the profile type is not possible through this serializer.
    """
    user = RegisterUserSerializer(read_only=True)

    class Meta :
        ref_name = None
        model = Profile
        fields = ('id', 'type', 'charge', 'user', )
        read_only_fields = ('id', 'type', 'user', )

    def validate(self, data) :
        user = self.context['request'].user
        if not user.profile :
            raise serializers.ValidationError(_("Bad Request"))

        data['charge'] = user.profile.charge + data['charge']
        return data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['type'] = utils.ProfileType.all_types()[ret['type']]
        return ret

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.user = self.context['request'].user
        instance.save()
        return instance


class CustomProfileSerializer (serializers.ModelSerializer) :
    user = RegisterUserSerializer(read_only=True)

    class Meta :
        ref_name = None
        model = CustomProfile
        exclude = ('created', 'updated', )
        read_only_fields = ('id', 'user', )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['gender'] = utils.GenderType.all_types()[ret['gender']]
        ret['education'] = utils.EducationLevel.all_types()[ret['education']]
        ret['employment'] = utils.EmploymentStatus.all_types()[ret['employment']]
        ret['tobacco'] = utils.TobaccoUsage.all_types()[ret['tobacco']]
        ret['alcohol'] = utils.AlcoholUsage.all_types()[ret['alcohol']]
        ret['physical_activity'] = utils.PhysicalActivity.all_types()[ret['physical_activity']]
        ret['fruit_consumption'] = utils.FruitConsumption.all_types()[ret['fruit_consumption']]
        ret['vegetable_consumption'] = utils.VegetableConsumption.all_types()[ret['vegetable_consumption']]
        ret['meat_consumption'] = utils.MeatConsumption.all_types()[ret['meat_consumption']]
        ret['obesity'] = utils.Obesity.all_types()[ret['obesity']]
        ret['sedentary_job'] = utils.SedentaryJob.all_types()[ret['sedentary_job']]
        ret['diabetes_history'] = utils.DiabetesHistory.all_types()[ret['diabetes_history']]
        ret['cholesterol_history'] = utils.CholesterolHistory.all_types()[ret['cholesterol_history']]
        ret['blood_pressure_history_on_mother_side'] = utils.BloodPressureHistory.all_types()[ret['blood_pressure_history_on_mother_side']]
        ret['blood_pressure_history_on_father_side'] = utils.BloodPressureHistory.all_types()[ret['blood_pressure_history_on_father_side']]
        ret['salty_diet'] = utils.SaltyDiet.all_types()[ret['salty_diet']]

        return ret
    
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.user = self.context['request'].user
        instance.save()
        return instance





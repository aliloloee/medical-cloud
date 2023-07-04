from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from profiles import utils


User = get_user_model()

class Profile(models.Model) :
    user = models.OneToOneField(
                            User, on_delete=models.CASCADE, unique=True,
                            null=True, blank=True,
                            related_name='profile', verbose_name=_('User')
                            )

    type = models.PositiveSmallIntegerField(
                            choices=utils.ProfileType.choices, default=utils.ProfileType.STANDARD,
                            verbose_name=_('Type')
                            )

    charge = models.DecimalField(
                            max_digits=11, decimal_places=2,
                            validators=[MinValueValidator(0.00)],
                            default=0.00,
                            verbose_name=_('Charge')
                            )

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))

    def type_in_string (self):
        return dict(utils.ProfileType.choices)[self.type].upper()

    class Meta :
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
        ordering = ('created',)

    def __str__(self):
        return _('Profile of {}').format(self.user)


class CustomProfile(models.Model) :
    user = models.OneToOneField(
                            User, on_delete=models.CASCADE, unique=True,
                            null=True, blank=True,
                            related_name='custom_profile', verbose_name=_('User')
                            )

    age = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Age'))

    gender = models.PositiveSmallIntegerField(
                            choices=utils.GenderType.choices, default=utils.GenderType.MALE,
                            verbose_name=_('Gender')
                            )
    
    education = models.PositiveSmallIntegerField(
                            choices=utils.EducationLevel.choices, default=utils.EducationLevel.BELOW_HIGHSCHOOL,
                            verbose_name=_('Education Level')
                            )
    
    employment = models.PositiveSmallIntegerField(
                            choices=utils.EmploymentStatus.choices, default=utils.EmploymentStatus.UNEMPLOYED,
                            verbose_name=_('Employment status')
                            )
    
    tobacco = models.SmallIntegerField(
                            choices=utils.TobaccoUsage.choices, default=utils.TobaccoUsage.NO,
                            verbose_name=_('Tobacco Usage')
                            )
    
    alcohol = models.SmallIntegerField(
                            choices=utils.AlcoholUsage.choices, default=utils.AlcoholUsage.NO,
                            verbose_name=_('Alcohol consumption')
                            )
    
    physical_activity = models.SmallIntegerField(
                            choices=utils.PhysicalActivity.choices, default=utils.PhysicalActivity.NEVER,
                            verbose_name=_('Physical activity')
                            )
    
    fruit_consumption = models.PositiveSmallIntegerField(
                            choices=utils.FruitConsumption.choices, default=utils.FruitConsumption.LOW,
                            verbose_name=_('Fruit consumption')
                            )
    
    vegetable_consumption = models.PositiveSmallIntegerField(
                            choices=utils.VegetableConsumption.choices, default=utils.VegetableConsumption.LOW,
                            verbose_name=_('Vegetable consumption')
                            )
    
    meat_consumption = models.PositiveSmallIntegerField(
                            choices=utils.MeatConsumption.choices, default=utils.MeatConsumption.LOW,
                            verbose_name=_('Meat consumption')
                            )
    
    obesity = models.PositiveSmallIntegerField(
                            choices=utils.Obesity.choices, default=utils.Obesity.THIN,
                            verbose_name=_('Obesity')
                            )
    
    sedentary_job = models.SmallIntegerField(
                            choices=utils.SedentaryJob.choices, default=utils.SedentaryJob.NO,
                            verbose_name=_('Sedentary job')
                            )
    
    diabetes_history = models.SmallIntegerField(
                            choices=utils.DiabetesHistory.choices, default=utils.DiabetesHistory.NO,
                            verbose_name=_('Diabetes history')
                            )
    
    cholesterol_history = models.SmallIntegerField(
                            choices=utils.CholesterolHistory.choices, default=utils.CholesterolHistory.NO,
                            verbose_name=_('Cholesterol history')
                            )
    
    blood_pressure_history_on_mother_side = models.SmallIntegerField(
                            choices=utils.BloodPressureHistory.choices, default=utils.BloodPressureHistory.NO,
                            verbose_name=_('Blood pressure history from mother side')
                            )
    
    blood_pressure_history_on_father_side = models.SmallIntegerField(
                            choices=utils.BloodPressureHistory.choices, default=utils.BloodPressureHistory.NO,
                            verbose_name=_('Blood pressure history from father side')
                            )
    
    salty_diet = models.SmallIntegerField(
                            choices=utils.SaltyDiet.choices, default=utils.SaltyDiet.NO,
                            verbose_name=_('Salty diet')
                            )

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))

    class Meta :
        verbose_name = _('Custom Profile')
        verbose_name_plural = _('Custom Profiles')
        ordering = ('created',)

    def __str__(self):
        return _('Custom profile of {}').format(self.user)
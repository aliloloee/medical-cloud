from django.db import models
from django.conf import settings


class ProfileType (models.IntegerChoices) :
    STANDARD = settings.STANDARD
    PRO      = settings.PRO
    ADVANCED = settings.ADVANCED
    FREE     = settings.FREE

    @classmethod
    def all_types(cls):
        return {
            cls.STANDARD.value : cls.STANDARD.label,
            cls.PRO.value : cls.PRO.label,
            cls.ADVANCED.value : cls.ADVANCED.label,
            cls.FREE.value : cls.FREE.label
        }

    @classmethod
    def allowed_types(cls):
        return {
            cls.STANDARD.value : cls.STANDARD.label,
            cls.PRO.value : cls.PRO.label,
            cls.ADVANCED.value : cls.ADVANCED.label
        }


class GenderType (models.IntegerChoices) :
    MALE     = settings.STANDARD
    FEMALE   = settings.PRO
    OTHER    = settings.ADVANCED

    @classmethod
    def all_types(cls):
        return {
            cls.MALE.value : cls.MALE.label,
            cls.FEMALE.value : cls.FEMALE.label,
            cls.OTHER.value : cls.OTHER.label
        }


class EducationLevel (models.IntegerChoices) :
    BELOW_HIGHSCHOOL  = settings.BELOW_HIGHSCHOOL
    HIGHSCHOOL        = settings.HIGHSCHOOL
    ABOVE_HIGHSCHOOL  = settings.ABOVE_HIGHSCHOOL

    @classmethod
    def all_types(cls):
        return {
            cls.BELOW_HIGHSCHOOL.value : cls.BELOW_HIGHSCHOOL.label,
            cls.HIGHSCHOOL.value : cls.HIGHSCHOOL.label,
            cls.ABOVE_HIGHSCHOOL.value : cls.ABOVE_HIGHSCHOOL.label
        }


class EmploymentStatus (models.IntegerChoices) :
    UNEMPLOYED  = settings.UNEMPLOYED
    EMPLOYED    = settings.EMPLOYED
    RETIRED     = settings.RETIRED

    @classmethod
    def all_types(cls):
        return {
            cls.UNEMPLOYED.value : cls.UNEMPLOYED.label,
            cls.EMPLOYED.value : cls.EMPLOYED.label,
            cls.RETIRED.value : cls.RETIRED.label
        }


class TobaccoUsage (models.IntegerChoices) :
    YES = settings.YES
    NO  =  settings.NO

    @classmethod
    def all_types(cls):
        return {
            cls.YES.value : cls.YES.label,
            cls.NO.value : cls.NO.label
        }


class AlcoholUsage (models.IntegerChoices) :
    YES = settings.YES
    NO  =  settings.NO

    @classmethod
    def all_types(cls):
        return {
            cls.YES.value : cls.YES.label,
            cls.NO.value : cls.NO.label
        }


class PhysicalActivity (models.IntegerChoices) :
    NEVER     = settings.NEVER
    SELDOM    = settings.SELDOM
    REGULAR   = settings.REGULAR

    @classmethod
    def all_types(cls):
        return {
            cls.NEVER.value : cls.NEVER.label,
            cls.SELDOM.value : cls.SELDOM.label,
            cls.REGULAR.value : cls.REGULAR.label
        }


class FruitConsumption (models.IntegerChoices) :
    LOW       = settings.LOW
    AVERAGE   = settings.AVERAGE
    HIGH      = settings.HIGH

    @classmethod
    def all_types(cls):
        return {
            cls.LOW.value : cls.LOW.label,
            cls.AVERAGE.value : cls.AVERAGE.label,
            cls.HIGH.value : cls.HIGH.label
        }


class VegetableConsumption (models.IntegerChoices) :
    LOW       = settings.LOW
    AVERAGE   = settings.AVERAGE
    HIGH      = settings.HIGH

    @classmethod
    def all_types(cls):
        return {
            cls.LOW.value : cls.LOW.label,
            cls.AVERAGE.value : cls.AVERAGE.label,
            cls.HIGH.value : cls.HIGH.label
        }


class MeatConsumption (models.IntegerChoices) :
    LOW       = settings.LOW
    AVERAGE   = settings.AVERAGE
    HIGH      = settings.HIGH

    @classmethod
    def all_types(cls):
        return {
            cls.LOW.value : cls.LOW.label,
            cls.AVERAGE.value : cls.AVERAGE.label,
            cls.HIGH.value : cls.HIGH.label
        }


class Obesity (models.IntegerChoices) :
    THIN               = settings.THIN
    FIT                = settings.FIT
    OVERWEIGHT         = settings.OVERWEIGHT
    EXTREME_OVERWEIGHT = settings.EXTREME_OVERWEIGHT

    @classmethod
    def all_types(cls):
        return {
            cls.THIN.value : cls.THIN.label,
            cls.FIT.value : cls.FIT.label,
            cls.OVERWEIGHT.value : cls.OVERWEIGHT.label,
            cls.EXTREME_OVERWEIGHT.value : cls.EXTREME_OVERWEIGHT.label
        }


class DiabetesHistory (models.IntegerChoices) :
    YES = settings.YES
    NO  =  settings.NO

    @classmethod
    def all_types(cls):
        return {
            cls.YES.value : cls.YES.label,
            cls.NO.value : cls.NO.label
        }


class CholesterolHistory (models.IntegerChoices) :
    YES = settings.YES
    NO  =  settings.NO

    @classmethod
    def all_types(cls):
        return {
            cls.YES.value : cls.YES.label,
            cls.NO.value : cls.NO.label
        }


class BloodPressureHistory (models.IntegerChoices) :
    YES = settings.YES
    NO  =  settings.NO

    @classmethod
    def all_types(cls):
        return {
            cls.YES.value : cls.YES.label,
            cls.NO.value : cls.NO.label
        }


class SedentaryJob (models.IntegerChoices) :
    YES = settings.YES
    NO  =  settings.NO

    @classmethod
    def all_types(cls):
        return {
            cls.YES.value : cls.YES.label,
            cls.NO.value : cls.NO.label
        }


class SaltyDiet (models.IntegerChoices) :
    YES = settings.YES
    NO  =  settings.NO

    @classmethod
    def all_types(cls):
        return {
            cls.YES.value : cls.YES.label,
            cls.NO.value : cls.NO.label
        }



def custom_profile_categorical_values():
    response = dict()
    response[GenderType.__name__]             = GenderType.all_types()
    response[EducationLevel.__name__]         = EducationLevel.all_types()
    response[EmploymentStatus.__name__]       = EmploymentStatus.all_types()
    response[TobaccoUsage.__name__]           = TobaccoUsage.all_types()
    response[AlcoholUsage.__name__]           = AlcoholUsage.all_types()
    response[PhysicalActivity.__name__]       = PhysicalActivity.all_types()
    response[FruitConsumption.__name__]       = FruitConsumption.all_types()
    response[VegetableConsumption.__name__]   = VegetableConsumption.all_types()
    response[MeatConsumption.__name__]        = MeatConsumption.all_types()
    response[Obesity.__name__]                = Obesity.all_types()
    response[DiabetesHistory.__name__]        = DiabetesHistory.all_types()
    response[CholesterolHistory.__name__]     = CholesterolHistory.all_types()
    response[BloodPressureHistory.__name__]   = BloodPressureHistory.all_types()
    response[SedentaryJob.__name__]           = SedentaryJob.all_types()
    response[SaltyDiet.__name__]              = SaltyDiet.all_types()

    return response
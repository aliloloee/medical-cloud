from rest_framework import filters
from django.db import models
from django.conf import settings


class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user=request.user)


class GenderType (models.IntegerChoices) :
    MALE     = settings.MALE
    FEMALE   = settings.FEMALE
    OTHER    = settings.OTHER

    @classmethod
    def all_types(cls):
        return {
            cls.MALE.value : cls.MALE.label,
            cls.FEMALE.value : cls.FEMALE.label,
            cls.OTHER.value : cls.OTHER.label
        }


class BloodTestArticles (models.IntegerChoices) :
    CBC               = settings.CBC
    ESR               = settings.ESR
    FBS               = settings.FBS
    TG                = settings.TG
    CHO               = settings.CHO
    BUN               = settings.BUN
    CREA              = settings.CREA
    SGOT              = settings.SGOT
    URIC_ACID         = settings.URIC_ACID
    SGPT              = settings.SGPT
    ALP               = settings.ALP
    BILI_T            = settings.BILI_T
    BILI_D            = settings.BILI_D
    T_PROTEIN         = settings.T_PROTEIN
    ALB               = settings.ALB
    MG                = settings.MG
    ZINC              = settings.ZINC
    VIT_D             = settings.VIT_D
    IRON              = settings.IRON
    TIBC              = settings.TIBC
    TSH               = settings.TSH
    T4                = settings.T4
    T3                = settings.T3
    CA                = settings.CA
    PHO               = settings.PHO
    NA                = settings.NA
    K                 = settings.K
    UA                = settings.UA
    UC                = settings.UC


    @classmethod
    def all_types(cls):
        return {
            cls.CBC.value       : cls.CBC.label,
            cls.ESR.value       : cls.ESR.label,
            cls.FBS.value       : cls.FBS.label,
            cls.TG.value        : cls.TG.label,
            cls.CHO.value       : cls.CHO.label,
            cls.BUN.value       : cls.BUN.label,
            cls.CREA.value      : cls.CREA.label,
            cls.SGOT.value      : cls.SGOT.label,
            cls.URIC_ACID.value : cls.URIC_ACID.label,
            cls.SGPT.value      : cls.SGPT.label,
            cls.ALP.value       : cls.ALP.label,
            cls.BILI_T.value    : cls.BILI_T.label,
            cls.BILI_D.value    : cls.BILI_D.label,
            cls.T_PROTEIN.value : cls.T_PROTEIN.label,
            cls.ALB.value       : cls.ALB.label,
            cls.MG.value        : cls.MG.label,
            cls.ZINC.value      : cls.ZINC.label,
            cls.VIT_D.value     : cls.VIT_D.label,
            cls.IRON.value      : cls.IRON.label,
            cls.TIBC.value      : cls.TIBC.label,
            cls.TSH.value       : cls.TSH.label,
            cls.T4.value        : cls.T4.label,
            cls.T3.value        : cls.T3.label,
            cls.CA.value        : cls.CA.label,
            cls.PHO.value       : cls.PHO.label,
            cls.NA.value        : cls.NA.label,
            cls.K.value         : cls.K.label,
            cls.UA.value        : cls.UA.label,
            cls.UC.value        : cls.UC.label,
        }


def check_up_categorical_values():
    response = dict()
    response[GenderType.__name__]             = GenderType.all_types()
    response[BloodTestArticles.__name__]      = BloodTestArticles.all_types()

    return response
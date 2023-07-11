from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from checkup import utils

import uuid

User = get_user_model()


class BloodTest(models.Model) :

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(
                    User, on_delete=models.CASCADE,
                    related_name='blood_tests', verbose_name=_('User')
                    )

    gender = models.PositiveSmallIntegerField(
                            choices=utils.GenderType.choices, default=utils.GenderType.MALE,
                            verbose_name=_('Gender')
                            )

    title = models.CharField(
                    max_length=100,
                    verbose_name=_('Blood test title')
                    )
    description = models.CharField(
                    max_length=300, blank=True,
                    verbose_name=_('blood test description')
                    )

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))


    class Meta :
        verbose_name = _('Blood test')
        verbose_name_plural = _('Blood tests')
        ordering = ('created',)

    def __str__(self):
        return self.title


class BloodTestResult(models.Model) :
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    blood_test = models.ForeignKey(
                    BloodTest, on_delete=models.CASCADE,
                    related_name='blood_test_results', verbose_name=_('Blood test')
                    )
    user = models.ForeignKey(
                    User, on_delete=models.CASCADE,
                    related_name='blood_test_results', verbose_name=_('User')
                    )
    
    name = models.PositiveIntegerField(
                            choices=utils.BloodTestArticles.choices,
                            verbose_name=_('Result name')
                            )

    value = models.DecimalField(max_digits=6, decimal_places=3, verbose_name=_('Result value'))

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))


    class Meta :
        verbose_name = _('Blood test result')
        verbose_name_plural = _('Blood test results')
        ordering = ('created',)

    def __str__(self):
        return str(utils.BloodTestArticles.all_types()[self.name])



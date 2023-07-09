from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from django_celery_beat.models import PeriodicTask

import uuid


User = get_user_model()


class UniversalPill(models.Model) :
    class BasedOnActivation(models.Manager) :
        def get_queryset(self) :
            return super().get_queryset().filter(is_active=True).order_by('created')
        
    class BasedOnInactivation(models.Manager) :
        def get_queryset(self) :
            return super().get_queryset().filter(is_active=False).order_by('created')

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(
                    max_length=100,
                    verbose_name=_('Pill name')
                    )

    description = models.CharField(
                    max_length=700, blank=True,
                    verbose_name=_('Pill description')
                    )
    
    application = models.CharField(
                    max_length=700, blank=True,
                    verbose_name=_('Pill application')
                    )

    is_active  = models.BooleanField(default=False, verbose_name=_('Pill is active'))

    objects = models.Manager()
    active_objects = BasedOnActivation()
    inactive_objects = BasedOnInactivation()

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))

    class Meta :
        verbose_name = _('Universal Pill')
        verbose_name_plural = _('Universal Pills')
        ordering = ('created',)

    def __str__(self):
        return f'Universal Pill {self.name}'


class Pill(models.Model) :

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(
                    User, on_delete=models.CASCADE, blank=True, null=True,
                    related_name='pill', verbose_name=_('User')
                    )
    name = models.CharField(
                    max_length=100,
                    verbose_name=_('Pill name')
                    )

    description = models.CharField(
                    max_length=700, blank=True,
                    verbose_name=_('Pill description')
                    )

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))

    class Meta :
        verbose_name = _('Pill')
        verbose_name_plural = _('Pills')
        ordering = ('created',)

    def __str__(self):
        return f'Pill of user {self.user} {self.name}'


class PillAlarm(models.Model) :

    class BasedOnActivation(models.Manager) :
        def get_queryset(self) :
            return super().get_queryset().filter(is_active=True).order_by('created')
        
    class BasedOnInactivation(models.Manager) :
        def get_queryset(self) :
            return super().get_queryset().filter(is_active=False).order_by('created')
        
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(
                    User, on_delete=models.CASCADE,
                    related_name='alarms', verbose_name=_('User')
                    )

    # Each pill can only have one alarm
    pill = models.OneToOneField(
                    Pill, on_delete=models.CASCADE,
                    related_name='alarms', verbose_name=_('Pill')
                    )

    periodic_task = models.ForeignKey(
                    PeriodicTask, on_delete=models.SET_NULL, blank=True, null=True,
                    related_name='alarms', verbose_name=_('Periodic Task')
                    )

    description = models.CharField(
                    max_length=700, blank=True,
                    verbose_name=_('Alarm description')
                    )

    objects = models.Manager()
    active_objects = BasedOnActivation()
    inactive_objects = BasedOnInactivation()

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))

    class Meta :
        verbose_name = _('Pill alarm')
        verbose_name_plural = _('Pill alarms')
        ordering = ('created',)

    def __str__(self):
        return f'Consumption alarm of {self.pill.name}, for user-id {self.user.pk}'


class AlarmNotification (models.Model) :
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(
                    User, on_delete=models.CASCADE,
                    related_name='notifications', verbose_name=_('User')
                    )

    alarm = models.ForeignKey(
                    PillAlarm, on_delete=models.CASCADE,
                    related_name='notifications', verbose_name=_('Alarm')
                    )
    consumed = models.BooleanField(default=True, verbose_name=_('Pill was consumed'))

    consumed_at = models.DateTimeField(verbose_name=_('Consumed at'))

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))

    class Meta :
        verbose_name = _('Pill notification')
        verbose_name_plural = _('Pill notifications')
        ordering = ('created',)

    def __str__(self):
        return f'Pill notification {self.id}'



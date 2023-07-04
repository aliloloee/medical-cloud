from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from datetime import datetime
from devices.utils import generate_api_key
import uuid

User = get_user_model()


class Device(models.Model) :

    class BasedOnActivation(models.Manager) :
        def get_queryset(self) :
            return super().get_queryset().filter(is_active=True).order_by('created')

    class BasedOnInactivation(models.Manager) :
        def get_queryset(self) :
            return super().get_queryset().filter(is_active=False).order_by('created')

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(
                    User, on_delete=models.CASCADE, blank=True, null=True,
                    related_name='devices', verbose_name=_('User')
                    )
    api_key = models.CharField(
                    max_length=100, default=generate_api_key, 
                    blank=True, verbose_name=_('API Key')
                    )
    name = models.CharField(
                    max_length=100,
                    verbose_name=_('Device name')
                    )
    description = models.CharField(
                    max_length=300, blank=True,
                    verbose_name=_('Device description')
                    )
    serial_number = models.CharField(
                    max_length=100,
                    unique=True,
                    verbose_name=_('Device serial')
                    )

    is_active  = models.BooleanField(default=False, verbose_name=_('Device is active'))

    objects = models.Manager()
    active_objects = BasedOnActivation()
    inactive_objects = BasedOnInactivation()

    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))

    class Meta :
        unique_together = ('user', 'name', )
        verbose_name = _('Device')
        verbose_name_plural = _('Devices')
        ordering = ('created',)

    def __str__(self):
        return self.name

class Record(models.Model) :
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    device = models.ForeignKey(
                    Device, on_delete=models.CASCADE,
                    related_name='records', verbose_name=_('Device')
                    )
    name = models.CharField(
                    max_length=100,
                    null=True,
                    verbose_name=_('Record name')
                    )

    data = models.JSONField()
    
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))

    class Meta :
        verbose_name = _('Record')
        verbose_name_plural = _('Records')
        ordering = ('created',)

    def save(self, *args, **kwargs) :
        if self._state.adding and self.name == None : # Record being created without name
            self.name = f'(no-title){datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name if self.name else str(self.created)
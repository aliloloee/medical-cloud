from django.contrib import admin
from .models import Device, Record

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin) :
    list_display = ('name', )
    readonly_fields = ('pk', 'api_key', )

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin) :
    list_display = ('name', )
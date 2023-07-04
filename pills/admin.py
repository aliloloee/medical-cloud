from django.contrib import admin
from .models import UniversalPill, Pill, PillAlarm, AlarmNotification


@admin.register(UniversalPill)
class UniversalPillAdmin(admin.ModelAdmin) :
    list_display = ('name', 'id', )


@admin.register(Pill)
class PillAdmin(admin.ModelAdmin) :
    list_display = ('name', 'related_user', 'id')

    @admin.display(description='user')
    def related_user(self, obj) :
        return f'{obj.user}'


@admin.register(PillAlarm)
class PillAlarmAdmin(admin.ModelAdmin) :
    list_display = ('related_user', 'related_pill', 'id', )

    @admin.display(description='user')
    def related_user(self, obj) :
        return f'{obj.user}'
    
    @admin.display(description='pill')
    def related_pill(self, obj) :
        return f'{obj.pill.name}'


admin.site.register(AlarmNotification)
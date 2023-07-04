from django.contrib import admin
from .models import Profile, CustomProfile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin) :
    list_display = ('related_user', 'type', )

    @admin.display(description='user')
    def related_user(self, obj) :
        return f'{obj.user}'

@admin.register(CustomProfile)
class CustomProfileAdmin(admin.ModelAdmin) :
    list_display = ('related_user', 'age', )

    @admin.display(description='user')
    def related_user(self, obj) :
        return f'{obj.user}'


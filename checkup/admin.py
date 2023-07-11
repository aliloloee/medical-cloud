from django.contrib import admin
from .models import BloodTest, BloodTestResult


@admin.register(BloodTest)
class BloodTestAdmin(admin.ModelAdmin) :
    list_display = ('title', 'id', )


@admin.register(BloodTestResult)
class BloodTestResultAdmin(admin.ModelAdmin) :
    list_display = ('name', 'related_test', 'id')

    @admin.display(description='blood test')
    def related_test(self, obj) :
        return f'{obj.blood_test}'
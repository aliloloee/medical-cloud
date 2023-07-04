from rest_framework.routers import DefaultRouter
from django.urls import path
from devices import views


app_name = 'devices'


router = DefaultRouter()
router.register('api/device', views.DeviceViewSet)


urlpatterns = [
    path('api/activate/<uuid:device_id>/', views.ActivateDeviceAPI.as_view(), name='api-activate-device'),
    path('api/override/<uuid:device_id>/', views.OverrideAPIKey.as_view(), name='override-device-api-key'),
    path('api/latest/', views.DeviceLatestRecordAPI.as_view(), name='latest-records'),
    #* Remaining urls --> related to device model
    # delete a device (Archive device with all data) --> Maybe deleting process should be banned !!
        # because then the user (based on it's profile type) can create another device
    # ........
]


urlpatterns += router.urls
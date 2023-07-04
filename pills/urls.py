from rest_framework.routers import DefaultRouter
from django.urls import path
from pills import views


app_name = 'pills'


router = DefaultRouter()
# A viewset that has a customized "get_queryset" method and no "queryset" argument, needs this "basename" argument
router.register('api/universal-pills', views.UniversalPillModelViewSet, basename='universal-pill')
router.register('api/pills', views.PillModelViewSet)
router.register('api/alarm', views.PillAlarmViewSet)
router.register('api/notification', views.AlarmNotificationViewSet)



urlpatterns = [
    path('api/search-universal-pill/<str:keyword>/', views.UniversalPillLookUpAPIView.as_view(), name='api-univesal-pill-look-up'),
]


urlpatterns += router.urls
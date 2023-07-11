from rest_framework.routers import DefaultRouter
from django.urls import path
from checkup import views


app_name = 'checkup'


router = DefaultRouter()
router.register('api/blood-test', views.BloodTestViewSet)
router.register('api/blood-test-detail', views.BloodTestDetailsViewSet)
router.register('api/blood-test-result', views.BloodTestResultsViewSet)


urlpatterns = [
    path('api/check-up/values/', views.CheckUpCategoricalValuesAPI.as_view(), name='api-check-up-vlaues'),
]


urlpatterns += router.urls
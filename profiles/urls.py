from django.urls import path
from profiles import views


app_name = 'profiles'


urlpatterns = [
    path('api/profile/', views.ProfileAPI.as_view(), name='api-profile'),
    path('api/profile/charge/', views.ProfileChargeAPI.as_view(), name='api-profile-charge'),
    path('api/custom-profile/', views.CustomProfileAPI.as_view(), name='api-custom-profile'),
    path('api/custom-profile/update/', views.CustomProfileUpdateAPI.as_view(), name='api-custom-profile-update'),
    path('api/custom-profile/values/', views.CustomProfileCategoricalValuesAPI.as_view(), name='api-custom-profile-vlaues'),
    #* Remaining urls
    # Swicth profile type
    # Charge account (increase charge of profile)
    # Retrieve allowed types
]
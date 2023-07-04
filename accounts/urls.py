from django.urls import path
from accounts import views


app_name = 'accounts'

urlpatterns = [
    path('api/user/', views.RegisterAPIView.as_view(), name='api-user'),
    path('api/verify/<str:token>/<str:hub_id>/', views.VerifyAPIView.as_view(), name='api-verify'),
    path('api/login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/change/password/', views.PasswordChangeAPIView.as_view(), name='api-change-password'),
    path('api/forget/password/', views.ForgetPasswordAPIView.as_view(), name='api-forget-password'),
    path('api/reset/<str:token>/<str:hub_id>/', views.ResetPasswordAPIView.as_view(), name='api-reset-password'),
    path('api/logout/', views.LogoutAPIView.as_view(), name='api-logout'),
    ## * check https://dj-rest-auth.readthedocs.io/en/latest/api_endpoints.html
    ## * remained endpoints
    # resend email
    # logout #? Celery-beat action remaining for clearing expired refresh tokens
    # user --> return user's information
    # verify token
]


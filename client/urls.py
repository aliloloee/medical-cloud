from django.urls import path
from client import views


app_name = 'clients'

urlpatterns = [
    path('live/', views.live, name='live'),
]


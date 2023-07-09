from django.urls import path
from client import consumers
from pills import consumers as pills_consumers



websocket_urlpatterns = [
    path('ws/live/send/', consumers.LiveDataConsumer.as_asgi(), name='send-live-data'),
    path('ws/live/receive/', consumers.LiveDataDistributer.as_asgi(), name='receive-live-data'),


    # Pill App websockets
    path('ws/notification/', pills_consumers.PillNotificationConsumer.as_asgi(), name='send-notification'),
]
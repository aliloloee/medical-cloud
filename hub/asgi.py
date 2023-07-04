import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hub.settings.development')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hub.settings.production')

django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from client import routings as client_routings



django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                client_routings.websocket_urlpatterns
            )
        )
    ),
})

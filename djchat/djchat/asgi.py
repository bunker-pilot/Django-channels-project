import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.middleware import JwtCookieAuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djchat.settings")
django_application = get_asgi_application()

from chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": django_application,
        "websocket": JwtCookieAuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        ),
    }
)
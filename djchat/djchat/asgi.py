import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djchat.settings")
django_application = get_asgi_application()

from chat.routing import ws_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": django_application,
        "websocket": URLRouter(ws_urlpatterns),
    }
)
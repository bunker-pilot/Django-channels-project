from django.urls import path
from .consumer import ChatConsumer


websocket_urlpatterns = [
    path("ws/chat/server/<int:server_id>/channel/<int:channel_id>/", ChatConsumer.as_asgi()),
]


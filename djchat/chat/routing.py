from django.urls import path
from .consumer import MyConsumer

ws_urlpatterns =[
    path("ws/test", MyConsumer.as_asgi())
]
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("servers", viewset= views.ServerViewSet)

app_name = "server"

urlpatterns = [
    path("", include(router.urls))
]

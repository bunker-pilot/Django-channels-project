from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("categories", viewset=views.CategoryViewSet, basename="category")
router.register("servers", viewset= views.ServerViewSet, basename="server")

app_name = "server"

urlpatterns = [
    path("", include(router.urls))
]

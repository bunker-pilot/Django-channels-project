from rest_framework import serializers
from .models import Category, Server, Channel


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = "__all__"
        read_only_fields = ["id"]
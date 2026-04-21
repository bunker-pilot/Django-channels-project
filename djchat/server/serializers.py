from rest_framework import serializers
from .models import Category, Server, Channel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ["id" , "name","owner"]


class ServerSerializer(serializers.ModelSerializer):
    channels = ChannelSerializer(many=True, read_only = True)
    category = CategorySerializer(read_only =True)
    member_count = serializers.SerializerMethodField()
    class Meta:
        model = Server
        fields = ["id" ,"owner","category", "name","member_count","description","channels"]
        read_only_fields = ["id", "owner"]

    def get_member_count(self, obj):
        if hasattr(obj, "member_count"):
            return obj.member_count
        return None
    
    def to_representation(self, instance):
        data= super().to_representation(instance)

        if not self.context.get("request")["inlcude_member_count"]:
            data.pop("member_count", None)
        return data
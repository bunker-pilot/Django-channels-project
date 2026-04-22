from rest_framework import serializers
from .models import Category, Server, Channel


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category model"""
    class Meta:
        model = Category
        fields = ["id", "name", "banner"]

class ChannelSerializer(serializers.ModelSerializer):
    """Serializer for channel model"""
    class Meta:
        model = Channel
        fields = ["id" , "name","owner"]


class ServerSerializer(serializers.ModelSerializer):
    """Serializer for server model"""
    channels = ChannelSerializer(many=True, read_only = True)
    category = CategorySerializer(read_only =True)
    member_count = serializers.SerializerMethodField()
    class Meta:
        model = Server
        fields = ["id" ,"owner","category", "icon","name","member_count","description","channels"]
        read_only_fields = ["id", "owner"]

    def get_member_count(self, obj):
        if hasattr(obj, "member_count"):
            return obj.member_count
        return None
    
    def to_representation(self, instance):
        data= super().to_representation(instance)
        
        if not self.context.get("include_member_count", False):
            data.pop("member_count", None)
        return data
    
class ServerIconSerializer(serializers.ModelSerializer):
    """Serializer for uploading icons to Servers"""
    class Meta:
        model = Server
        fields =["id", "icon"]
        read_only_fields = ["id"]
        extra_kwargs = {"icon" : {"required":"True"}}
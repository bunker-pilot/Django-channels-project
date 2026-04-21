from django.shortcuts import render
from django.db.models import Count
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .models import Server
from .schema import server_extend_schema, server_user_extend_schema
# Create your views here.

@server_extend_schema
class ServerViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """ViewSet for managing Server API"""
    serializer_class = serializers.ServerSerializer

    def get_queryset(self):
        category_id = self.request.query_params.get("category_id")
        qty = self.request.query_params.get("qty")
        num_member = self.request.query_params.get("num_member")
        queryset = Server.objects.all()
        if category_id:
            # Filter servvers by category
            queryset = queryset.filter(category__id = category_id)
        
        if qty:
            try:
                qty = int(qty)
                if qty>0:
                    queryset = queryset[: int(qty)]
            except ValueError:
                pass
        if num_member:
            queryset = queryset.annotate(member_count = Count("member"))
        
        return queryset
    
    def get_serializer_context(self):
        context= super().get_serializer_context()
        include_member_count = "num_member" in self.request.query_params
        context["include_member_count"] = include_member_count
        return context
    

    @server_user_extend_schema
    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated] )
    def my_servers(self, request):
        """Get servers where the user is a member"""
        servers = Server.objects.filter(member = self.request.user)

        category_id = request.query_params.get("category_id")
        if category_id:
            #Filter servers by category
            servers = servers.filter(category__id = category_id)
        
        serializer = serializers.ServerSerializer(servers,many= True)
        return Response(serializer.data)

    @action(methods=["POST"], detail=True, permission_classes=[IsAuthenticated], url_path="join")
    def join_server(self, request, pk=None):
        """Add user as a member to the server"""
        server = self.get_object()
        if request.user not in server.member.all():
            server.member.add(request.user)
            return Response({"status":"joined"}, status=200)
        return Response({"status": "Already a member"}, status=200)
    
    @action(methods=["POST"] , detail=True, permission_classes=[IsAuthenticated], url_path="leave")
    def leave_server(self, request, pk=None):
        """Leave a server"""
        server = self.get_object()
        if request.user ==server.owner:
            return Response({"status": "You can't leave your own server"}, status=400)
        if request.user in server.member.all():
            server.member.remove(request.user)
            return Response({"status":"Left"}, status=200)
        return Response({"status":"not a member"}, status=200)
    
    @action(methods=["POST"] , detail=True, url_path="upload-icon", permission_classes=[IsAuthenticated])
    def upload_icon(self, request, pk=None):
        """Upload Server's icon"""
        server = self.get_object()
        
        serializer = self.get_serializer(server, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    

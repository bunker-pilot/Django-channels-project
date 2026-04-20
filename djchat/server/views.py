from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from . import serializers
from .models import Server
# Create your views here.

class ServerViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()
    
    def get_queryset(self):
        category_id = self.query_params.get("category_id")
        queryset = self.queryset
        if category_id:
            queryset = queryset.filter(category__id= category_id)
        
        return queryset
            
    
    def list(self, request):    
        serializer = serializers.ServerSerializer(self.queryset, many=True)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


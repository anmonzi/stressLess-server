"""View module for handling requests about resources"""
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from stresslessapi.models import Resource, AppUser


class ResourceSerializer(serializers.ModelSerializer):
    """JSON serializer for resources"""
    class Meta:
        model = Resource
        fields = '__all__'


class ResourceView(ViewSet):
    """App resource viewset"""

    def list(self, request):
        """Handle GET requests to resource data table"""
        # verify user and who is making request
        app_user = AppUser.objects.get(user=request.auth.user)

        resources = Resource.objects.all()

        serializer = ResourceSerializer(resources, many=True, context={'request': request})
        return Response(serializer.data)

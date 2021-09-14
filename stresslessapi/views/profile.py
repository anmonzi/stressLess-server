"""View module for handling requests about user profile"""
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from stresslessapi.models import AppUser


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for users"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)


class AppUserSerializer(serializers.ModelSerializer):
    """JSON serializer for app users"""
    user = UserSerializer(many=False)

    class Meta:
        model = AppUser
        fields = ('user', 'full_name')


class Profile(ViewSet):
    """App user profile information"""

    def list(self, request):
        """Handle GET requests to profile resource"""

        app_user = AppUser.objects.get(user=request.auth.user)

        app_user = AppUserSerializer(app_user, many=False, context={'request': request})

        # Manually constructing the JSON structure returned in response
        profile = {}
        profile['app_user'] = app_user.data

        return Response(profile)

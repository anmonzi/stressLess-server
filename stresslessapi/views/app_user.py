"""View module for handling requests about user profile"""
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from stresslessapi.models import AppUser


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for users"""
    class Meta:
        model = User
        fields = ('username', 'email', 'is_active', 'date_joined',
            'last_login', 'is_staff')


class AppUserSerializer(serializers.ModelSerializer):
    """JSON serializer for app users"""
    user = UserSerializer(many=False)

    class Meta:
        model = AppUser
        fields = ('user', 'full_name')


class AppUserView(ViewSet):
    """App user information"""

    def list(self, request):
        """Handle GET requests to app user resource"""

        # verify user and who is making request
        app_user = AppUser.objects.get(user=request.auth.user)

        users = AppUser.objects.all()

        serializer = AppUserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)

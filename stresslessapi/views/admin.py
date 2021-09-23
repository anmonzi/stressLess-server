"""View module for handling requests about user as admin"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers
from django.db.models import Case, When, Count
from stresslessapi.models import AppUser


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for users"""
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'date_joined',
            'is_staff', 'is_active')


class AppUserSerializer(serializers.ModelSerializer):
    """JSON serializer for app users"""
    user = UserSerializer(many=False)

    class Meta:
        model = AppUser
        fields = ('id', 'user', 'full_name', 'bio', 'image_url')




class AdminView(ViewSet):
    """StressLess admin viewset"""

    def list(self, request):
        """Handle GET requests to profile resource"""

        # verify user and who is making request
        app_user = AppUser.objects.get(user=request.auth.user)

        users = AppUser.objects.all()

        serializer = AppUserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['put',], detail=True)
    def deactivate(self, request, pk=None):
        """deactivate a user"""

        if request.method == "PUT":
            try:
                user = User.objects.get(pk=pk)
                user.is_active = not user.is_active
                user.save()
                serializer = UserSerializer(user, many=False, context={'request': request})
                return Response(serializer.data)
            except User.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as ex:
                return HttpResponseServerError(ex)

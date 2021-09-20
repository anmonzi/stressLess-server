"""View module for handling requests about users"""
from rest_framework.permissions import DjangoModelPermissions
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User 
from django.core.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for users
    """
    class Meta:
        model = User
        fields = ('is_staff',)


class UserView(ViewSet):
    """StressLess User View"""

    def list(self, request):
        """Handle GET requests for users
        """
        try:
            user = User.objects.get(pk=request.auth.user_id)
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

"""View module for handling requests about admin motivations"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from stresslessapi.models import Motivation, AppUser


class MotivationSerializer(serializers.ModelSerializer):
    """JSON serializer for motivations"""
    class Meta:
        model = Motivation
        fields = '__all__'


class MotivationView(ViewSet):
    """App motivation viewset"""

    def list(self, request):
        """Handle GET requests to motivation data table"""
        # verify user and who is making request
        app_user = AppUser.objects.get(user=request.auth.user)

        motivations = Motivation.objects.all().order_by('-id')[0]


        serializer = MotivationSerializer(motivations, many=False, context={'request': request})
        return Response(serializer.data)


    def create(self, request):
        """Handle POST operations for new motivations"""

        # verify user and who is making post request
        app_user = AppUser.objects.get(user=request.auth.user)

        # create new instance of motivation
        motivation = Motivation()
        motivation.app_user = app_user
        motivation.title = request.data["title"]
        motivation.content = request.data["content"]
        motivation.created_on = request.data["createdOn"]

        try:
            motivation.save()
            serializer = MotivationSerializer(motivation, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

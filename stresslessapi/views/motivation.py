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

    def retrieve(self, request, pk=None):
        """Handle GET request for single motivation"""
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/priorities/2
            #
            # The `2` at the end of the route becomes `pk`
            motivation = Motivation.objects.get(pk=pk)
            serializer = MotivationSerializer(motivation, context={'request': request})
            return Response(serializer.data)
        except Motivation.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT request sent for a motivation"""

        # verify user and who is making put request
        app_user = AppUser.objects.get(user=request.auth.user)

        # grab post to be updated by pk
        motivation = Motivation.objects.get(pk=pk)
        motivation.app_user = app_user
        motivation.title = request.data["title"]
        motivation.content = request.data["content"]
        motivation.created_on = request.data["createdOn"]

        motivation.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single motivation"""
        try:
            motivation = Motivation.objects.get(pk=pk)
            motivation.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Motivation.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def list(self, request):
        """Handle GET requests to motivation data table"""
        # verify user and who is making request
        app_user = AppUser.objects.get(user=request.auth.user)

        motivations = Motivation.objects.all()

        if "sortBy" in request.query_params:
            attr = request.query_params["sortBy"]
            if attr == "date":
                motivation = motivations.order_by('-id')[0]
                serializer = MotivationSerializer(motivation, many=False, context={'request': request})
                return Response(serializer.data)

        serializer = MotivationSerializer(motivations, many=True, context={'request': request})
        return Response(serializer.data)


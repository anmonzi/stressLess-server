"""View module for handling requests about user reflections"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.db.models.fields import BooleanField
from rest_framework import serializers
from django.db.models import Case, When
from stresslessapi.models import Reflection, AppUser


class ReflectionSerializer(serializers.ModelSerializer):
    """JSON serializer for reflections"""

    class Meta:
        model = Reflection
        fields = ('id', 'app_user', 'content',
            'created_on', 'owner')


class ReflectionView(ViewSet):
    """StressLess reflections viewset for create, read, delete"""

    def create(self, request):
        """"Handle POST operations for reflections"""

        # verify user and who is making post request
        app_user = AppUser.objects.get(user=request.auth.user)

        # create new instance of reflection
        reflection = Reflection()
        reflection.app_user = app_user
        reflection.content = request.data["content"]
        reflection.created_on = request.data["createdOn"]

        try:
            reflection.save()
            serializer = ReflectionSerializer(reflection, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single reflection"""
        try:
            reflection = Reflection.objects.get(pk=pk)
            reflection.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Reflection.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self,request):
        """Handle GET requests for reflections"""
        # verify user and who is making put request
        app_user = AppUser.objects.get(user=request.auth.user)

        # get all reflections from the database (works 9/15)
        # reflections = Reflection.objects.all()

        # get all priorities from the database that correspond to the current user
        reflections = Reflection.objects.annotate(owner=Case(
                                                When(app_user=app_user, then=True),
                                                default=False,
                                                output_field=BooleanField()
                                            ))

        serializer = ReflectionSerializer(
            reflections, many=True, context={'request': request})
        return Response(serializer.data)

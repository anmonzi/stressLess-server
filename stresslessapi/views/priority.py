"""View module for handling requests about user priorities"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.db.models.fields import BooleanField
from rest_framework import serializers
from django.db.models import Case, When
from stresslessapi.models import Priority, AppUser


class PrioritySerializer(serializers.ModelSerializer):
    """JSON serializer for priorites"""

    class Meta:
        model = Priority
        fields = ('id', 'app_user', 'content',
          'created_on', 'completed', 'owner')
        depth = 1


class PriorityView(ViewSet):
    """StressLess priorities viewset for create, read, update, delete"""

    def create(self, request):
        """Handle POST operations for priorities"""

        # verify user and who is making post request
        app_user = AppUser.objects.get(user=request.auth.user)

        # create new instance of priority
        priority = Priority()
        priority.app_user = app_user
        priority.content = request.data["content"]
        priority.created_on = request.data["createdOn"]
        priority.completed = request.data["completed"]

        try:
            priority.save()
            serializer = PrioritySerializer(priority, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """"Handle GET request for single priority"""
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/priorities/2
            #
            # The `2` at the end of the route becomes `pk`
            priority = Priority.objects.get(pk=pk)
            serializer = PrioritySerializer(priority, context={'request': request})
            return Response(serializer.data)
        except Priority.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def update(self, request, pk=None):
        """Handle PUT request sent for a priority"""

        # verify user and who is making put request
        app_user = AppUser.objects.get(user=request.auth.user)

        # grab priority to be updated by pk
        priority = Priority.objects.get(pk=pk)
        priority.app_user = app_user
        priority.content = request.data["content"]
        priority.created_on = request.data["createdOn"]
        priority.completed = request.data["completed"]

        priority.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single priority"""
        # grab priority to be deleted by pk
        try:
            priority = Priority.objects.get(pk=pk)
            priority.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Priority.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def list(self, request):
        """Handle GET requests to priorities"""
        # verify user and who is making put request
        app_user = AppUser.objects.get(user=request.auth.user)

        # get all priorities from the database (works 9/14)
        # priorities = Priority.objects.all()

        # get all priorities from the database that correspond to the current user
        priorities = Priority.objects.annotate(owner=Case(
                                                When(app_user=app_user, then=True),
                                                default=False,
                                                output_field=BooleanField()
                                            ))

        serializer = PrioritySerializer(
            priorities, many=True, context={'request': request})
        return Response(serializer.data)

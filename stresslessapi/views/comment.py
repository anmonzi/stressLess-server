"""View module for handling requests about user posts"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.db.models.fields import BooleanField
from rest_framework import serializers
from django.db.models import Case, When
from stresslessapi.models import Comment, AppUser, Post


class CommentAppUserSerializer(serializers.ModelSerializer):
    """JSON serializer for comment owner"""

    class Meta:
        model = AppUser
        fields = ('id', 'full_name')

class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments"""
    app_user = CommentAppUserSerializer(many=False)
    
    class Meta:
        model = Comment
        fields = ('id', 'post_id', 'app_user', 'content',
                    'created_on', 'owner')
        depth = 1

class CommentView(ViewSet):
    """StressLess comment viewset for complete CRUD"""

    def create(self, request):
        """Handle POST operations for new comments"""

        # verify user and who is making post request
        app_user = AppUser.objects.get(user=request.auth.user)
        # grab post id comment is related to
        post = Post.objects.get(pk=request.data['postId'])

        # create a new instance of comment
        comment = Comment()
        comment.post = post
        comment.app_user = app_user
        comment.content = request.data["content"]
        comment.created_on = request.data["createdOn"]

        try:
            comment.save()
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        """Handle GET request for single comment"""
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except Comment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def update(self, request, pk=None):
        """Handle PUT request sent for a comment"""

        # verify user and who is making put request
        app_user = AppUser.objects.get(user=request.auth.user)
        # grab post id comment is related to
        post = Post.objects.get(pk=request.data['postId'])

        comment = Comment.objects.get(pk=pk)
        comment.post = post
        comment.app_user = app_user
        comment.content = request.data["content"]
        comment.created_on = request.data["createdOn"]

        comment.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single comment"""
        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Comment.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def list(self, request):
        """Handle GET requests to posts"""
        # verify user and who is making put request
        app_user = AppUser.objects.get(user=request.auth.user)
        # get all comments from the database (works 9/15)
        comments = Comment.objects.all()

        # get all comments from the database that correspond to the current user
        # comments = Comment.objects.annotate(owner=Case(
        #                                         When(app_user=app_user, then=True),
        #                                         default=False,
        #                                         output_field=BooleanField()
        #                                     ))

        post = self.request.query_params.get('postId', None)
        if post is not None:
            comments = comments.filter(post__id= post)

        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

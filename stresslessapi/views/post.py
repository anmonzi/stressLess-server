"""View module for handling requests about user posts"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.db.models.fields import BooleanField
from rest_framework import serializers
from rest_framework.decorators import action
from django.db.models import Case, When, Count
from stresslessapi.models import Post, AppUser, Comment, Reaction


class PostAppUserSerializer(serializers.ModelSerializer):
    """JSON serializer for comment owner"""

    class Meta:
        model = AppUser
        fields = ('id', 'full_name')

class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts"""
    app_user = PostAppUserSerializer(many=False)

    class Meta:
        model = Post
        fields = ('id', 'app_user', 'title', 'content',
            'image_url', 'publication_date', 'owner',
            'comment_count', 'reactions')
        depth = 1


class PostView(ViewSet):
    """StressLess posts viewset for complete CRUD"""

    def create(self, request):
        """Handle POST operations for new posts"""

        # verify user and who is making post request
        app_user = AppUser.objects.get(user=request.auth.user)

        # create new instance of post
        post = Post()
        post.app_user = app_user
        post.title = request.data["title"]
        post.content = request.data["content"]
        post.image_url = request.data["imageURL"]
        post.publication_date = request.data["publicationDate"]

        try:
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        """Handle GET request for single post"""
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/priorities/2
            #
            # The `2` at the end of the route becomes `pk`
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def update(self, request, pk=None):
        """Handle PUT request sent for a post"""

        # verify user and who is making put request
        app_user = AppUser.objects.get(user=request.auth.user)

        # grab post to be updated by pk
        post = Post.objects.get(pk=pk)
        post.app_user = app_user
        post.title = request.data["title"]
        post.content = request.data["content"]
        post.image_url = request.data["imageURL"]
        post.publication_date = request.data["publicationDate"]

        post.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single post"""
        # grab post to be deleted by pk
        try:
            post = Post.objects.get(pk=pk)
            post.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def list(self, request):
        """"Handle GET requests to posts"""
        # verify user and who is making put request
        app_user = AppUser.objects.get(user=request.auth.user)

        # get all posts from the database (works 9/15)
        # posts = Post.objects.all()

        # get all priorities from the database that correspond to the current user
        posts = Post.objects.annotate(comment_count=Count('comment'),
                                        owner=Case(
                                        When(app_user=app_user, then=True),
                                        default=False,
                                        output_field=BooleanField()
                                            ),
                                        reactions_count=Count('reactions'))

        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)

from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from stresslessapi.models import PostReaction, Reaction, AppUser, Post


class ReactionSerializer(serializers.ModelSerializer):
    """JSON serializer for reaction"""

    class Meta:
        model = Reaction
        fields = ('id', 'label', 'image_url')

class PostReactionSerializer(serializers.ModelSerializer):
    """JSON serializer for post reaction join table"""

    reaction = ReactionSerializer(many=False)

    class Meta:
        model = PostReaction
        fields = ('id', 'app_user', 'post', 'reaction')


class PostReactionView(ViewSet):
    """StressLess post reacions join table viewset"""
    def create(self, request):
        """Handle POST operations for post reaction table"""

        # verify user and who is making post request
        app_user = AppUser.objects.get(user=request.auth.user)

        post_reaction = PostReaction()
        post_reaction.app_user = app_user
        post_reaction.post = Post.objects.get(pk=request.data["post"])
        post_reaction.reaction = Reaction.objects.get(pk=request.data["reaction"])

        try:
            post_reaction.save()
            serializer = PostReactionSerializer(post_reaction, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    # def update(self, request, pk=None):
    #     post_reaction = PostReaction.objects.get(pk=pk)
    #     post_reaction.rare_user = RareUser.objects.get(user=request.auth.user)
    #     post_reaction.post = Post.objects.get(pk=request.data["post"])
    #     post_reaction.reaction = Reaction.objects.get(pk=request.data["reaction"])
    #     post_reaction.save()

    #     return Response({}, status=status.HTTP_204_NO_CONTENT)

    # def retrieve(self, request, pk=None):
    #     try:
    #         post_reaction = PostReaction.objects.get(pk=pk)
    #         serializer = PostReactionSerializer(post_reaction, context={'request': request})
    #         return Response(serializer.data)
    #     except Exception as ex:
    #         return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for post reaction table"""
        try:
            post_reaction = PostReaction.objects.get(pk=pk)
            post_reaction.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Reaction.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET for post reaction join table"""
        # verify user and who is making put request
        app_user = AppUser.objects.get(user=request.auth.user)

        post_reactions = PostReaction.objects.all()
        # if app_user is not None:
        #     post_reactions = PostReaction.objects.filter(app_user__id=app_user)
        # #filtering post_reactions by post
        # else:
        #     post = self.request.query_params.get('post', None)
        #     if post is not None:
        #         post_reactions = PostReaction.objects.filter(post__id=post)

        #     else:
        #         post_reactions = PostReaction.objects.all()

        serializer = PostReactionSerializer(
            post_reactions, many=True, context={'request': request}
        )
        return Response(serializer.data)

from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from stresslessapi.models import Reaction


class ReactionSerializer(serializers.ModelSerializer):
    """JSON serializer for reaction"""
    class Meta:
        model = Reaction
        fields = ('id', 'label', 'image_url')
        depth = 1


class ReactionView(ViewSet):
    """StressLess reaction viewset"""

    def list(self, request):
        """Handle GET requests to reaction"""
        reactions = Reaction.objects.all()
        serializer = ReactionSerializer(
            reactions, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations for new reaction"""
        reaction = Reaction()
        reaction.label = request.data["label"]
        reaction.image_url = request.data["image_url"]
        try:
            reaction.save()
            serializer = ReactionSerializer(reaction, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """"Handle DELETE requests for a single reaction"""
        try:
            reaction = Reaction.objects.get(pk=pk)
            reaction.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Reaction.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Message
from .serializers import RecursiveMessageSerializer, MessageSerializer

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    user.delete()
    return Response({'detail': 'User and related data deleted successfully.'},status=status.HTTP_204_NO_CONTENT)


class ThreadedMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = Message.objects.filter(
            receiver=request.user,
            parent_message__isnull=True
        ).prefetch_related('replies', 'sender', 'receiver')
        serializer = RecursiveMessageSerializer(messages, many=True)
        return Response(serializer.data)


class UnreadMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        unread_messages = Message.unread.for_user(request.user)
        serializer = MessageSerializer(unread_messages, many=True)
        return Response(serializer.data)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Message
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db.models import Prefetch
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
            sender=request.user,
            parent_message__isnull=True
        ).select_related('sender', 'receiver').prefetch_related(Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver')))
        serializer = RecursiveMessageSerializer(messages, many=True)
        return Response(serializer.data)


class UnreadMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        unread_messages = Message.unread.unread_for_user(request.user).only('id', 'sender', 'content', 'timestamp', 'read').select_related('sender')
        serializer = MessageSerializer(unread_messages, many=True)
        return Response(serializer.data)

@method_decorator(cache_page(60), name='dispatch')
class ConversationMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = Message.objects.filter(receiver=request.user).order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

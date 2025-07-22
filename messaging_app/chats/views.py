from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here. ConversationViewSet MessageViewSet
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_querset(self):
        # Only show conversations where the current user is a participant
        return self.queryset.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get("participant_ids", [])
        if request.user.id not in participant_ids:
            participant_ids.append(request.user.id)

        participants = User.objects.filter(id__in=participant_ids)
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs.get("conversation_pk")
        conversation = get_object_or_404(Conversation, pk=conversation_id)

        if self.request.user not in conversation.participants.all():
            return Message.objects.none()

        return conversation.messages.all()

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get("conversation_pk")
        conversation = get_object_or_404(Conversation, pk=conversation_id)

        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant in this conversation.")

        serializer.save(sender=self.request.user, conversation=conversation)
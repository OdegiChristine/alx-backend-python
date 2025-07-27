from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Conversation, Message

class IsParticipantOfConversation(BasePermission):
    """
    Allow access only to authenticated users who are participants
    of a specific conversation (read/write/delete).
    """

    def has_permission(self, request, view):
        # Check global access for authenticated users only
        return request.user and request.user.is_authenticated

    def has_object_perrmission(self, request, view, obj):
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()
        if isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()
        return False

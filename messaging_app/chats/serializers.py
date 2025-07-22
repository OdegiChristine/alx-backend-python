from rest_framework import serializers
from .models import User, Message, Conversation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'first_name', 'last_name', 'email', 'role', 'phone_number')
        read_only_fields = ['user_id', 'role', 'email']


class MessageSerializer(serializers.ModelSerializer):
    sender =UserSerializer(read_only=True)

    class Meta:
        model = Message
        field = ['message_id', 'sender', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']
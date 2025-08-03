from rest_framework import serializers
from .models import Message

class RecursiveMessageSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'edited', 'replies']

    def get_replies(self, obj):
        return RecursiveMessageSerializer(obj.replies.all(), many=True).data


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp', 'read']

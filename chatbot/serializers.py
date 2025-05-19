from chatbot.models import Chat
from rest_framework import serializers


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['sender', 'message', 'timestamp']


class SessionSerializer(serializers.Serializer):
    session_id = serializers.CharField()
    messages = ChatSerializer(many=True)
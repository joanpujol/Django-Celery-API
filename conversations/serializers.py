from rest_framework import serializers

from . import models


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chat
        fields = "__all__"


class ConversationSerializer(serializers.ModelSerializer):
    chats = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = models.Conversation
        fields = "__all__"

from rest_framework import serializers

from . import models


class ChatSerializer(serializers.ModelSerializer):
    conversation_id = serializers.IntegerField(source='conversation.id')
    status = serializers.SerializerMethodField('get_status_display')

    class Meta:
        model = models.Chat
        fields = ('id', 'payload', 'conversation_id', 'created_date', 'status', )

    @staticmethod
    def get_status_display(obj):
        return obj.get_status_display()


class ConversationSerializer(serializers.ModelSerializer):
    store_id = serializers.IntegerField(source='store.id')
    operator_id = serializers.IntegerField(source='operator.id')
    operator_group = serializers.CharField(source='operator.operator_group.name')
    client_id = serializers.IntegerField(source='client.id')
    status = serializers.SerializerMethodField('get_status_display')
    chats = ChatSerializer(many=True, read_only=True)

    class Meta:
        model = models.Conversation
        fields = ('id', 'store_id', 'operator_id', 'operator_group', 'client_id', 'status', 'chats', )

    @staticmethod
    def get_status_display(obj):
        return obj.get_status_display()

from rest_framework import generics
from rest_framework import viewsets

from . import models
from . import serializers


class ConversationView(viewsets.ModelViewSet):
    queryset = models.Conversation.objects.all()

    def get_serializer_class(self):
        """Enables the endpoint to show mapped values while accepting the original model data when posting"""
        if self.action == 'create':
            return serializers.ConversationSerializer
        return serializers.ConversationDetailSerializer


class ConversationDetailView(generics.RetrieveAPIView):
    queryset = models.Conversation.objects.all()
    serializer_class = serializers.ConversationDetailSerializer


class ChatView(viewsets.ModelViewSet):
    queryset = models.Chat.objects.all()
    serializer_class = serializers.ChatSerializer

    def get_serializer_class(self):
        """Enables the endpoint to show mapped values while accepting the original model data when posting"""
        if self.action == 'create':
            return serializers.ChatSerializer
        return serializers.ChatDetailSerializer


class ChatDetailView(generics.RetrieveAPIView):
    queryset = models.Chat.objects.all()
    serializer_class = serializers.ChatDetailSerializer

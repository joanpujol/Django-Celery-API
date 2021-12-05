from rest_framework import generics

from . import models
from . import serializers


class ConversationView(generics.ListCreateAPIView):
    queryset = models.Conversation.objects.all()
    serializer_class = serializers.ConversationSerializer


class ConversationElementView(generics.RetrieveAPIView):
    queryset = models.Conversation.objects.all()
    serializer_class = serializers.ConversationSerializer


class ChatView(generics.ListCreateAPIView):
    queryset = models.Chat.objects.all()
    serializer_class = serializers.ChatSerializer


class ChatElementView(generics.RetrieveAPIView):
    queryset = models.Chat.objects.all()
    serializer_class = serializers.ChatSerializer

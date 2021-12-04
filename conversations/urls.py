from django.urls import path

from conversations import views

urlpatterns = [
    path('conversations/', views.ConversationView.as_view(), name='conversations'),
    path('conversations/<int:pk>', views.ConversationElementView.as_view(), name='conversations-detail'),
    path('chats/', views.ChatView.as_view(), name='chats'),
    path('chats/<int:pk>', views.ChatElementView.as_view(), name='chats-detail'),
]

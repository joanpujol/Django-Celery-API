from django.urls import path

from conversations import views

LIST_CREATE_ACTIONS = {'get': 'list', 'post': 'create'}

urlpatterns = [
    path('conversations/', views.ConversationView.as_view(LIST_CREATE_ACTIONS), name='conversations'),
    path('conversations/<int:pk>', views.ConversationDetailView.as_view(), name='conversations-detail'),
    path('chats/', views.ChatView.as_view(LIST_CREATE_ACTIONS), name='chats'),
    path('chats/<int:pk>', views.ChatDetailView.as_view(), name='chats-detail'),
]

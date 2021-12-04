from django.urls import path

from conversations import views

urlpatterns = [
    path('conversations/', views.ConversationView.as_view(), name='conversations'),
    path('conversations/<int:id>', views.ConversationElementView.as_view(), name='conversations-detail'),
]

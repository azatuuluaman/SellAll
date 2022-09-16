from django.urls import path

from chat.views import MessageAPIView, ChatAPIVIew, MessageReadAPIView

urlpatterns = [
    path('message/', MessageAPIView.as_view(), name='message'),
    path('chats/', ChatAPIVIew.as_view(), name='chat'),
    path('', MessageReadAPIView.as_view(), name='read_chat')
]

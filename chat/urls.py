from django.urls import path

from chat.views import MessageAPIView, ChatAPIVIew, MessageReadAPIView, MyChatsAPIView

urlpatterns = [
    path('', MessageReadAPIView.as_view(), name='read_chat'),
    path('message/', MessageAPIView.as_view(), name='message'),
    path('chats/', ChatAPIVIew.as_view(), name='chat'),
    path('my_chats/', MyChatsAPIView.as_view(), name='my_chats')
]

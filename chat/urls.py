from django.urls import path

from chat.views import MessageAPIView, ChatListAPIVIew, ChatAPIView, MyChatsAPIView

urlpatterns = [
    path('', ChatAPIView.as_view(), name='read_chat'),
    path('message/', MessageAPIView.as_view(), name='message'),
    path('chats/', ChatListAPIVIew.as_view(), name='chats'),
    path('my-chats/', MyChatsAPIView.as_view(), name='my_chats'),
    # path('chat/', MessagesAPIView.as_view(), name='chat')
]

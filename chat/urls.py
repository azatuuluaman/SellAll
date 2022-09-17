from django.urls import path

from chat.views import MessageAPIView, ChatAPIVIew, MessageReadAPIView, PusherVerifyAPIView

urlpatterns = [
    path('', MessageReadAPIView.as_view(), name='read_chat'),
    path('message/', MessageAPIView.as_view(), name='message'),
    path('chats/', ChatAPIVIew.as_view(), name='chat'),
    path('verify/', PusherVerifyAPIView.as_view(), name='pusher_verify'),
]

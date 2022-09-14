from django.urls import path

from chat.views import MessageAPIView, ChatAPIVIew

urlpatterns = [
    path('message/', MessageAPIView.as_view(), name='message'),
    path('chats/', ChatAPIVIew.as_view(), name='chat'),
]
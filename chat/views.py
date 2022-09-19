from django.contrib.auth import get_user_model
from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import views
from rest_framework.permissions import IsAuthenticated

from advertisement.models import Advertisement
from .models import Chat, Message
from .pusher import pusher_client
from .serializers import MessageSerializer, ChatListSerializer, ChatSerializer

User = get_user_model()


class MessageAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(method='post',
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['version'],
                             properties={
                                 'ads_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                 'message': openapi.Schema(type=openapi.TYPE_STRING),
                             },
                             operation_description='Send message'))
    @action(['post'], detail=False)
    def post(self, request):
        ads_id = request.data.get('ads_id')
        ads = get_object_or_404(Advertisement, pk=ads_id)

        user = request.user

        chat_id = f'{ads.pk}-{ads.owner_id}-{user.pk}'
        message = request.data.get('message')

        chat = Chat.objects.get_or_create(chat_id=chat_id, advertisement_id=ads_id)[0]
        instance = Message.objects.create(sender=user, chat=chat, message=message)

        serializer = MessageSerializer(instance)
        data = serializer.data

        pusher_client.trigger(chat.chat_id, 'message', data)

        if Message.objects.filter(chat=chat).count() == 1:
            pusher_client.trigger(f'my-chats-count-{user.pk}', 'message', f'{chat.chat_id}')

        return Response(data, status=status.HTTP_200_OK)


class ChatAPIVIew(views.APIView):
    serializer_class = ChatListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        ChatSerializer(queryset)

    def get_queryset(self):
        owner = Q(advertisement__owner=self.request.user)
        sender = Q(messages__sender=self.request.user)
        return Chat.objects.filter(owner | sender).distinct()


class MessageReadAPIView(views.APIView):
    @swagger_auto_schema(method='post', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['version'],
        properties={
            'chat_id': openapi.Schema(type=openapi.TYPE_STRING),
        },
        operation_description='Read message in chat'))
    @action(methods=['POST'], detail=False)
    def post(self, request, *args, **kwargs):
        chat_id = request.data.get('chat_id')

        if not chat_id:
            return Response({'chat_id': "Field chat_id can't be empty"}, status=status.HTTP_400_BAD_REQUEST)

        messages = Message.objects.exclude(sender=request.user.pk)

        messages.filter(chat__chat_id=chat_id, is_read=False).update(is_read=True)

        return Response({'message': 'Success'}, status=status.HTTP_200_OK)


class MyChatsAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        # count = Chat.objects.filter(advertisement__owner=user).count()
        return Response({'channel': f'my-chats-count-{user.pk}'}, status=status.HTTP_200_OK)

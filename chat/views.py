import json

from django.contrib.auth import get_user_model
from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import views, generics
from rest_framework.permissions import IsAuthenticated

from advertisement.models import Advertisement
from advertisement.swagger_scheme import chat_id
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
                                 'chat_id': openapi.Schema(type=openapi.TYPE_STRING),
                                 'message': openapi.Schema(type=openapi.TYPE_STRING),
                             },
                             operation_description='Send message'))
    @action(['post'], detail=False)
    def post(self, request):
        ads_id = request.data.get('ads_id')
        user = request.user
        user_id = user.pk

        chat_id_query = request.data.get('chat_id')

        if chat_id_query:
            if '-' not in chat_id_query:
                return Response({'chat_id': "Not valid!"}, status=status.HTTP_400_BAD_REQUEST)

            ads_id, user_id = chat_id_query.split('-')

        ads = get_object_or_404(Advertisement, pk=ads_id)

        chat_id = f'{ads.pk}-{user_id}'

        message = request.data.get('message')

        chat = Chat.objects.get_or_create(chat_id=chat_id, advertisement_id=ads_id, sender_id=user_id)[0]
        instance = Message.objects.create(sender=user, chat=chat, message=message)

        serializer = MessageSerializer(instance)
        data = serializer.data

        pusher_client.trigger(chat.chat_id, 'message', data)

        if Message.objects.filter(chat=chat).count() == 1:
            pusher_client.trigger(f'my-chats-count-{user.pk}', 'message', f'{chat.chat_id}')

        return Response(data, status=status.HTTP_200_OK)


class ChatListAPIVIew(generics.ListAPIView):
    serializer_class = ChatListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        owner = Q(advertisement__owner=self.request.user)
        sender = Q(messages__sender=self.request.user)
        return Chat.objects.filter(owner | sender).distinct()


class ChatAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(method='get', manual_parameters=[chat_id])
    @action(methods=['GET'], detail=False)
    def get(self, request, *args, **kwargs):
        chat_id = request.query_params.get('chat_id')

        if not chat_id:
            return Response({'chat_id': "Field chat_id can't be empty"}, status=status.HTTP_400_BAD_REQUEST)

        chat = get_object_or_404(Chat, chat_id=chat_id)
        messages = Message.objects.filter(chat=chat)

        response_data = {message.send_date.strftime('%d.%m.%Y'): [] for message in messages}

        for message in messages:
            response_data[message.send_date.strftime('%d.%m.%Y')].append(MessageSerializer(message).data)

        messages_is_read = Message.objects.exclude(sender=request.user.pk)

        messages_is_read.filter(chat=chat, is_read=False).update(is_read=True)
        data = ChatSerializer(chat).data

        return Response(
            {
                'chat': data,
                'messages_parts': response_data
            }, status=status.HTTP_200_OK)


class MyChatsAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        return Response({'channel': f'my-chats-count-{user.pk}'}, status=status.HTTP_200_OK)

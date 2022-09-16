from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticated

from advertisement.models import Advertisement
from .models import Chat, Message
from .pusher import pusher_client
from .serializers import MessageSerializer, ChatSerializer


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

        if not Advertisement.objects.filter(pk=ads_id).exists():
            return Response({'message': 'The advertisement not found!'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        chat_id = f'private-{ads_id}-{user.pk}'
        message = request.data.get('message')

        chat = Chat.objects.get_or_create(chat_id=chat_id, advertisement_id=ads_id)[0]
        instance = Message.objects.create(sender=user, chat=chat, message=message)

        serializer = MessageSerializer(instance)
        data = serializer.data

        pusher_client.trigger(chat.chat_id, 'message', data)

        return Response(data, status=status.HTTP_200_OK)


class ChatAPIVIew(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        owner = Q(advertisement__owner=self.request.user)
        sender = Q(messages__sender=self.request.user)
        return Chat.objects.filter(owner | sender)


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

        Message.objects.filter(chat__chat_id=chat_id, is_read=False).update(is_read=True)

        return Response({'message': 'Success'}, status=status.HTTP_200_OK)


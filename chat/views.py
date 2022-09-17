from django.contrib.auth import get_user_model
from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

from advertisement.models import Advertisement
from .models import Chat, Message
from .pusher import pusher_client
from .serializers import MessageSerializer, ChatSerializer

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

        chat_id = f'private-{ads_id}-{ads.owner_id}'
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

        Message.objects.filter(chat__chat_id=chat_id, is_read=False).update(is_read=True)

        return Response({'message': 'Success'}, status=status.HTTP_200_OK)


class PusherVerifyAPIView(views.APIView):
    @swagger_auto_schema(method='post', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['version'],
        properties={
            'token': openapi.Schema(type=openapi.TYPE_STRING),
        },
        operation_description='Verify token'))
    @action(methods=['POST'], detail=False)
    def post(self, request, *args, **kwargs):
        token = request.data.get('token')

        if not token:
            return Response({"token": "Токен обязательное поле"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            access_token = AccessToken(token)
        except TokenError:
            return Response({"detail": "Токен недействителен или просрочен", "code": "token_not_valid"},
                            status=status.HTTP_401_UNAUTHORIZED)

        User.objects.get(pk=access_token['user_id'])

        return Response({"auth": token}, status=status.HTTP_200_OK)

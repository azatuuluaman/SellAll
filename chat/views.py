from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from advertisement.models import Advertisement
from .models import Chat, Message
from .pusher import pusher_client
from .serializers import MessageSerializer


class MessageAPIView(APIView):
    permission_classes = [IsAuthenticated]

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

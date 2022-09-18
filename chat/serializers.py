from rest_framework import serializers

from advertisement.serializers import AdvertisementRetrieveSerializer
from .models import Message, Chat


class MessageSerializer(serializers.ModelSerializer):
    chat = serializers.CharField(source='chat.chat_id', read_only=True)
    sender = serializers.CharField(source='sender.__str__', read_only=True)

    class Meta:
        model = Message
        fields = (
            'sender',
            'chat',
            'message',
            'send_date',
            'is_read',
        )


class ChatSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField(read_only=True)
    unread_count = serializers.SerializerMethodField(read_only=True)
    advertisement_name = serializers.CharField(source='advertisement.name', read_only=True)

    def get_unread_count(self, obj):
        messages = Message.objects.exclude(sender=self.context.get('request').user.pk)
        message_count = messages.filter(chat=obj, is_read=False).count()
        return message_count

    def get_message(self, obj):
        instance = Message.objects.filter(chat=obj).last()
        serializer = MessageSerializer(instance)
        data = serializer.data
        del data['chat']
        return data

    class Meta:
        model = Chat
        fields = (
            'chat_id',
            'advertisement',
            'advertisement_name',
            'message',
            'unread_count',
        )

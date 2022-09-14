from rest_framework import serializers

from .models import Message, Chat


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = (
            'sender',
            'chat',
            'message',
            'send_date'
        )


class ChatSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField(read_only=True)

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
            'message',
        )

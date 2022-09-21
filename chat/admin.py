from django.contrib import admin

from .models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat_id', 'advertisement')
    list_display_links = ('id', 'chat_id')
    list_filter = ('advertisement',)
    search_fields = ('advertisement',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'chat', 'get_message')
    list_display_links = ('id', 'sender')
    list_filter = ('sender', 'chat', 'send_date')
    search_fields = ('message',)

    def get_message(self, obj):
        """
        Метод для получение картинки в виде отрендеренного html
        """
        return obj.message[:150]

    get_message.short_description = 'Сообщение'

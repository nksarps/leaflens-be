from chatbot.models import Chat
from django.contrib import admin

class ChatAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'sender', 'timestamp')

admin.site.register(Chat, ChatAdmin)
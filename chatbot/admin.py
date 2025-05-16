from chatbot.models import Chat
from django.contrib import admin

class ChatAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'user')

admin.site.register(Chat, ChatAdmin)
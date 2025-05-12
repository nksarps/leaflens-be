from accounts.models import User
from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'username', 'is_verified')
    readonly_fields = ('created_at',)

admin.site.register(User, UserAdmin)
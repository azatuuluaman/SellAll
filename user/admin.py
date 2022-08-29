from django.contrib import admin
from .models import User


@admin.register(User)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'phone_number', 'is_superuser')
    list_display_links = ('id', 'email')
    readonly_fields = ('created', 'modified', 'last_login')
    search_fields = ('email', 'first_name', 'last_name')

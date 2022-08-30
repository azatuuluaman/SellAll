from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'phone_number', 'is_staff', 'is_superuser', 'is_active')
    list_display_links = ('id', 'email')
    readonly_fields = ('created', 'modified', 'last_login')
    search_fields = ('email', 'first_name', 'last_name')
    list_editable = ('is_staff', 'is_superuser', 'is_active')

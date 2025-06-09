from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_staff')
    search_fields = ('email', 'username')  # Поиск по email и имени
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)
    filter_horizontal = ()
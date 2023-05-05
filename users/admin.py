from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'date_joined', 'is_active', 'is_staff',)
    search_fields = ('email', 'username', 'first_name', 'last_name',)
    ordering = ('email', 'username',)


admin.site.register(CustomUser, CustomUserAdmin)
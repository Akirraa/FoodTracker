from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'last_login', 'is_active',)
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ()

    fieldsets = (
        (None, {
            'fields': (
                'username', 'password', 'email', 'first_name', 'last_name',
                 'weight', 'height', 'age', 'is_active',
                'is_staff', 'is_superuser'
            ),
        }),
        ('Permissions', {
            'fields': ('groups', 'user_permissions'),
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined'),
        }),
    )
    
admin.site.register(User, UserAdmin)

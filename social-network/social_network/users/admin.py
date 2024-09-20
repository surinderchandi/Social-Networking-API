from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    model = User
    # Define the fields to be displayed in the list view
    list_display = ('email', 'is_staff', 'is_active')
    
    # Define the fields to be included in the user creation and editing forms
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )
    
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, UserAdmin)

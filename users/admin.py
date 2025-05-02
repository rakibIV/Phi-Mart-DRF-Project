from django.contrib import admin
from users.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields' : ('email', 'password')}),
        ('personal_info', {'fields' : ('first_name', 'last_name', 'address', 'phone_number')}),
        ('Permissions', {'fields' : ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields' : ('last_login', 'date_joined')})
        
        
    )
    
    add_fieldsets = (
        (None, {
            'classes' : ('wide',),
            'fields' : ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')
        }),
    )
    
    search_fields = ('email',)
    ordering = ('email',)
    
admin.site.register(User, CustomUserAdmin)
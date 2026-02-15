from django.contrib import admin
from .models import UserProfile 

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_full_name', 'role', 'department', 'phone', 'created_at')
    list_filter = ('role', 'department')
    search_fields = ('user__username', 'user__email', 'roll_number')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'phone')
        }),
        ('Academic Information', {
            'fields': ('roll_number', 'department', 'role')
        }),
        ('Profile Picture', {
            'fields': ('profile_image',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def user_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    user_full_name.short_description = 'User'
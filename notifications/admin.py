from django.contrib import admin
from django.utils.html import format_html
from .models import Notification, Announcement

# Register your models here.

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_username', 'notification_type', 'read_badge', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'title', 'message')
    readonly_fields = ('created_at',)
    
    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'User'
    
    def read_badge(self, obj):
        color = '#4caf50' if obj.is_read else '#f44336'
        text = 'Read' if obj.is_read else 'Unread'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            text
        )
    read_badge.short_description = 'Read Status'


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority_badge', 'created_by', 'expires_at', 'created_at')
    list_filter = ('priority', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')
    
    def priority_badge(self, obj):
        colors = {'low': '#4caf50', 'normal': '#2196f3', 'high': '#ff9800', 'urgent': '#f44336'}
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            colors.get(obj.priority, '#999'),
            obj.get_priority_display()
        )
    priority_badge.short_description = 'Priority'
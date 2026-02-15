from django.contrib import admin
from .models import Event, EventRegistration

# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'event_date', 'capacity_display', 'organizer')
    list_filter = ('category', 'event_date')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Event Details', {
            'fields': ('title', 'description', 'category', 'location', 'image')
        }),
        ('Scheduling', {
            'fields': ('event_date', 'end_date')
        }),
        ('Registration', {
            'fields': ('capacity', 'registered_count', 'organizer')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def capacity_display(self, obj):
        percentage = (obj.registered_count / obj.capacity * 100) if obj.capacity > 0 else 0
        return f"{obj.registered_count}/{obj.capacity} ({percentage:.0f}%)"
    capacity_display.short_description = 'Registration'


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'event_title', 'registration_date', 'attended_badge')
    list_filter = ('attended', 'registration_date')
    search_fields = ('user__username', 'event__title')
    readonly_fields = ('registration_date',)
    
    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'User'
    
    def event_title(self, obj):
        return obj.event.title
    event_title.short_description = 'Event'
    
    def attended_badge(self, obj):
        color = '#4caf50' if obj.attended else '#f44336'
        text = 'Attended' if obj.attended else 'Not Attended'
        from django.utils.html import format_html
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            text
        )
    attended_badge.short_description = 'Status'

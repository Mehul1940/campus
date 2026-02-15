from django.contrib import admin
from django.utils.html import format_html
from .models import LostAndFound

# Register your models here.

@admin.register(LostAndFound)
class LostAndFoundAdmin(admin.ModelAdmin):
    list_display = ('item_type', 'item_status_badge', 'status_badge', 'location', 'report_date')
    list_filter = ('item_status', 'status', 'report_date')
    search_fields = ('item_type', 'description', 'location')
    readonly_fields = ('report_date', 'claim_date')
    
    fieldsets = (
        ('Item Information', {
            'fields': ('item_type', 'item_status', 'description', 'location', 'date_found_lost')
        }),
        ('Status', {
            'fields': ('status', 'image')
        }),
        ('Claim Details', {
            'fields': ('claimed_by', 'claim_date'),
            'classes': ('collapse',)
        }),
        ('Report Details', {
            'fields': ('reported_by', 'report_date'),
            'classes': ('collapse',)
        }),
    )
    
    def item_status_badge(self, obj):
        color = '#ff9800' if obj.item_status == 'lost' else '#2196f3'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.get_item_status_display()
        )
    item_status_badge.short_description = 'Item Status'
    
    def status_badge(self, obj):
        colors = {'open': '#f44336', 'claimed': '#ff9800', 'returned': '#4caf50'}
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, '#999'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
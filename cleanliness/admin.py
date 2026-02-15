from django.contrib import admin
from django.utils.html import format_html
from .models import CleanlinessReport

# Register your models here.

@admin.register(CleanlinessReport)
class CleanlinessReportAdmin(admin.ModelAdmin):
    list_display = ('report_id', 'location', 'severity_badge', 'status_badge', 'report_date')
    list_filter = ('severity', 'status', 'report_date')
    search_fields = ('location', 'issue_description')
    readonly_fields = ('report_date', 'resolved_date')
    
    fieldsets = (
        ('Report Information', {
            'fields': ('reported_by', 'location', 'issue_description', 'image')
        }),
        ('Severity & Status', {
            'fields': ('severity', 'status')
        }),
        ('Assignment & Resolution', {
            'fields': ('assigned_to', 'feedback', 'report_date', 'resolved_date')
        }),
    )
    
    def report_id(self, obj):
        return f"#{obj.id}"
    report_id.short_description = 'Report'
    
    def severity_badge(self, obj):
        colors = {'low': '#4caf50', 'medium': '#ff9800', 'high': '#f44336', 'critical': '#9c27b0'}
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            colors.get(obj.severity, '#999'),
            obj.get_severity_display()
        )
    severity_badge.short_description = 'Severity'
    
    def status_badge(self, obj):
        colors = {'open': '#f44336', 'in_progress': '#ff9800', 'resolved': '#4caf50'}
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, '#999'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
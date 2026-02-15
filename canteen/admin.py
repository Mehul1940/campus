from django.contrib import admin
from django.utils.html import format_html
from .models import CanteenMenu, FoodOrder, OrderItem

# Register your models here.

@admin.register(CanteenMenu)
class CanteenMenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'formatted_price', 'available', 'preparation_time')
    list_filter = ('category', 'available')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'image')
        }),
        ('Pricing & Availability', {
            'fields': ('price', 'available', 'preparation_time')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def formatted_price(self, obj):
        return f"Rs. {obj.price}"
    formatted_price.short_description = 'Price'


@admin.register(FoodOrder)
class FoodOrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user_username', 'status_badge', 'total_amount', 'order_time')
    list_filter = ('status', 'order_time')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('order_time', 'total_amount')
    
    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'status', 'total_amount', 'order_time')
        }),
        ('Timing', {
            'fields': ('pickup_time',)
        }),
        ('Additional', {
            'fields': ('special_instructions',)
        }),
    )
    
    def order_id(self, obj):
        return f"#{obj.id}"
    order_id.short_description = 'Order'
    
    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'User'
    
    def status_badge(self, obj):
        colors = {
            'pending': '#ff9800',
            'preparing': '#2196f3',
            'ready': '#4caf50',
            'completed': '#8bc34a',
            'cancelled': '#f44336',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, '#999'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'menu_item', 'quantity', 'item_price')
    list_filter = ('order__status',)
    search_fields = ('order__id', 'menu_item__name')
    
    def order_id(self, obj):
        return f"Order #{obj.order.id}"
    order_id.short_description = 'Order'
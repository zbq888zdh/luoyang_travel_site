from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Attraction, TourPackage, Order, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']

@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'ticket_price', 'view_count', 'is_recommended']
    list_filter = ['category', 'is_recommended']
    search_fields = ['name', 'address']
    list_editable = ['ticket_price', 'is_recommended']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'category', 'description')
        }),
        ('位置信息', {
            'fields': ('address', 'latitude', 'longitude')
        }),
        ('票务信息', {
            'fields': ('ticket_price', 'opening_hours', 'phone')
        }),
        ('其他设置', {
            'fields': ('image', 'is_recommended', 'view_count')
        }),
    )

@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'price', 'duration_days', 'is_active']
    list_filter = ['type', 'is_active']
    search_fields = ['name']
    filter_horizontal = ['attractions']  # 方便选择包含的景点

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_no', 'user', 'total_amount', 'status', 'travel_date', 'created_at']
    list_filter = ['status', 'travel_date']
    search_fields = ['order_no', 'contact_name', 'contact_phone']
    readonly_fields = ['order_no', 'created_at', 'updated_at']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['attraction', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']

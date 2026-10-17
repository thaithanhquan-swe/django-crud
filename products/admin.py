from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'price', 'quantity', 'status', 'created_at')
    list_filter = ('category', 'status', 'created_at')
    search_fields = ('name', 'sku', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'sku', 'category', 'description')
        }),
        ('Giá & Tồn kho', {
            'fields': ('price', 'quantity')
        }),
        ('Hình ảnh & Trạng thái', {
            'fields': ('image', 'status')
        }),
        ('Thời gian', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

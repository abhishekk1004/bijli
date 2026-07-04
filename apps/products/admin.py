from django.contrib import admin

from apps.common.admin import ImagePreviewMixin
from apps.products.models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'image_preview', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    readonly_fields = ['image_preview']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'caption', 'order']


@admin.register(Product)
class ProductAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_featured', 'is_active', 'order', 'image_preview', 'created_at']
    list_filter = ['is_active', 'is_featured', 'category', 'created_at']
    search_fields = ['name', 'short_description', 'description']
    list_editable = ['price', 'is_featured', 'is_active', 'order']
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['category']
    ordering = ['order', 'name']
    readonly_fields = ['image_preview']
    inlines = [ProductImageInline]
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'category', 'is_active', 'is_featured', 'order')}),
        ('Content', {'fields': ('short_description', 'description', 'image', 'image_preview')}),
        ('Details', {'fields': ('price', 'features', 'specifications')}),
        ('SEO', {'fields': ('meta_title', 'meta_description', 'meta_keywords'), 'classes': ('collapse',)}),
    )

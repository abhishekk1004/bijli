from django.contrib import admin
from apps.services.models import Service, ServiceCategory
from apps.common.admin import ImagePreviewMixin


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']


@admin.register(Service)
class ServiceAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ['name', 'category', 'icon', 'is_featured', 'is_active', 'order', 'image_preview', 'created_at']
    list_filter = ['is_active', 'is_featured', 'category', 'created_at']
    search_fields = ['name', 'short_description', 'description']
    list_editable = ['is_featured', 'is_active', 'order']
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['category']
    ordering = ['order', 'name']
    readonly_fields = ['image_preview']
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'category', 'icon', 'is_active', 'is_featured', 'order')}),
        ('Content', {'fields': ('short_description', 'description', 'image', 'image_preview', 'features')}),
        ('SEO', {'fields': ('meta_title', 'meta_description', 'meta_keywords'), 'classes': ('collapse',)}),
    )

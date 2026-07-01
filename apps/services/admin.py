from django.contrib import admin
from apps.services.models import Service, ServiceCategory


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'icon', 'is_featured', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'is_featured', 'category', 'created_at']
    search_fields = ['name', 'short_description', 'description']
    list_editable = ['is_featured', 'is_active', 'order']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']

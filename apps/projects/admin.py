from django.contrib import admin

from apps.common.admin import ImagePreviewMixin
from apps.projects.models import Category, Project, ProjectImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ['image', 'caption', 'order']


@admin.register(Project)
class ProjectAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ['name', 'category', 'client', 'status', 'is_featured', 'is_active', 'order', 'image_preview', 'created_at']
    list_filter = ['is_active', 'is_featured', 'status', 'category', 'created_at']
    search_fields = ['name', 'client', 'location', 'short_description', 'description']
    list_editable = ['status', 'is_featured', 'is_active', 'order']
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['category']
    ordering = ['order', 'name']
    readonly_fields = ['image_preview']
    inlines = [ProjectImageInline]
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'category', 'status', 'is_active', 'is_featured', 'order')}),
        ('Content', {'fields': ('short_description', 'description', 'image', 'image_preview')}),
        ('Details', {'fields': ('client', 'location', 'start_date', 'end_date', 'budget', 'scope_of_work')}),
        ('SEO', {'fields': ('meta_title', 'meta_description', 'meta_keywords'), 'classes': ('collapse',)}),
    )

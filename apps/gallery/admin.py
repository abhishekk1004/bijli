from django.contrib import admin

from apps.common.admin import ImagePreviewMixin
from apps.gallery.models import Album, GalleryImage, GalleryVideo


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1
    fields = ['image', 'caption', 'order']


class GalleryVideoInline(admin.TabularInline):
    model = GalleryVideo
    extra = 0
    fields = ['title', 'video_url', 'thumbnail', 'order']


@admin.register(Album)
class AlbumAdmin(ImagePreviewMixin, admin.ModelAdmin):
    image_field_name = 'cover_image'
    list_display = ['title', 'order', 'is_active', 'image_preview', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['order', 'title']
    readonly_fields = ['image_preview']
    inlines = [GalleryImageInline, GalleryVideoInline]


@admin.register(GalleryImage)
class GalleryImageAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ['album', 'caption', 'order', 'image_preview', 'created_at']
    list_filter = ['album']
    search_fields = ['caption', 'album__title']
    list_editable = ['order']
    autocomplete_fields = ['album']
    readonly_fields = ['image_preview']


@admin.register(GalleryVideo)
class GalleryVideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'album', 'order', 'created_at']
    list_filter = ['album']
    search_fields = ['title', 'album__title']
    list_editable = ['order']
    autocomplete_fields = ['album']

from django.contrib import admin
from django.utils.html import format_html


class ImagePreviewMixin:
    """Adds a read-only thumbnail preview for a ModelAdmin's `image` field."""

    image_field_name = 'image'
    preview_height = 60

    @admin.display(description='Preview')
    def image_preview(self, obj):
        image = getattr(obj, self.image_field_name, None)
        if not image:
            return '—'
        return format_html(
            '<img src="{}" style="height:{}px;border-radius:4px;" />',
            image.url, self.preview_height,
        )


class SingletonAdminMixin:
    """Blocks adding a second row once one instance of a SingletonModel exists."""

    def has_add_permission(self, request):
        return not self.model.objects.exists()

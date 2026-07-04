from django.contrib import admin
from apps.core.models import (
    CompanyInfo, SocialMedia, NavbarLink, FooterSection,
    HeroSlider, Client, Testimonial, SEOSetting
)
from apps.common.admin import ImagePreviewMixin, SingletonAdminMixin


@admin.register(CompanyInfo)
class CompanyInfoAdmin(SingletonAdminMixin, ImagePreviewMixin, admin.ModelAdmin):
    image_field_name = 'logo'
    list_display = ("company_name", "email", "phone", "is_active", "image_preview")
    list_filter = ("is_active",)
    search_fields = ("company_name", "email")
    readonly_fields = ("image_preview",)
    fieldsets = (
        (None, {'fields': ('company_name', 'short_name', 'tagline', 'is_active')}),
        ('Branding', {'fields': ('logo', 'image_preview', 'favicon')}),
        ('Contact', {'fields': ('email', 'phone', 'secondary_phone', 'address', 'google_map')}),
        ('Footer', {'fields': ('copyright',)}),
    )


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ("platform", "url", "is_active", "order")
    list_filter = ("platform", "is_active")
    list_editable = ("order",)


@admin.register(NavbarLink)
class NavbarLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "parent", "is_active", "order")
    list_filter = ("is_active",)
    list_editable = ("order",)
    search_fields = ("title", "url")
    autocomplete_fields = ("parent",)


@admin.register(FooterSection)
class FooterSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "column", "order")
    list_editable = ("column", "order")
    filter_horizontal = ("links",)


@admin.register(HeroSlider)
class HeroSliderAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("title", "is_active", "order", "is_fullscreen", "image_preview")
    list_filter = ("is_active",)
    list_editable = ("order", "is_fullscreen")
    readonly_fields = ("image_preview",)


@admin.register(Client)
class ClientAdmin(ImagePreviewMixin, admin.ModelAdmin):
    image_field_name = 'logo'
    list_display = ("name", "website", "is_active", "order", "image_preview")
    list_filter = ("is_active",)
    list_editable = ("order",)
    search_fields = ("name",)
    readonly_fields = ("image_preview",)


@admin.register(Testimonial)
class TestimonialAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("client_name", "company", "rating", "is_active", "image_preview")
    list_filter = ("is_active", "rating")
    search_fields = ("client_name", "company", "message")
    readonly_fields = ("image_preview",)


@admin.register(SEOSetting)
class SEOSettingAdmin(admin.ModelAdmin):
    list_display = ("page_name", "meta_title", "is_active")
    list_filter = ("is_active",)
    search_fields = ("page_name", "meta_title")
    prepopulated_fields = {'slug': ('page_name',)}

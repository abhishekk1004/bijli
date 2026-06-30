from django.contrib import admin
from apps.core.models import (
    CompanyInfo, SocialMedia, NavbarLink, FooterSection,
    HeroSlider, Client, Testimonial, SEOSetting
)


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ("company_name", "email", "phone", "is_active")
    list_filter = ("is_active",)
    search_fields = ("company_name", "email")


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


@admin.register(FooterSection)
class FooterSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "column", "order")
    list_editable = ("column", "order")
    filter_horizontal = ("links",)


@admin.register(HeroSlider)
class HeroSliderAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "order", "is_fullscreen")
    list_filter = ("is_active",)
    list_editable = ("order", "is_fullscreen")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "website", "is_active", "order")
    list_filter = ("is_active",)
    list_editable = ("order",)
    search_fields = ("name",)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("client_name", "company", "rating", "is_active")
    list_filter = ("is_active", "rating")
    search_fields = ("client_name", "company", "message")


@admin.register(SEOSetting)
class SEOSettingAdmin(admin.ModelAdmin):
    list_display = ("page_name", "meta_title")
    search_fields = ("page_name", "meta_title")
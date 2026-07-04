from django.contrib import admin

from apps.about.models import About, ChairmanMessage, Milestone, Stat, TeamMember, FAQ
from apps.common.admin import ImagePreviewMixin, SingletonAdminMixin


@admin.register(About)
class AboutAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ['title', 'is_active', 'image_preview', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['image_preview']


@admin.register(ChairmanMessage)
class ChairmanMessageAdmin(SingletonAdminMixin, ImagePreviewMixin, admin.ModelAdmin):
    image_field_name = 'photo'
    list_display = ['name', 'designation', 'is_active', 'image_preview']
    readonly_fields = ['image_preview']


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ['year', 'title', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['year', 'title', 'description']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'year']


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ['number', 'label', 'icon', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['number', 'label']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'label']


@admin.register(TeamMember)
class TeamMemberAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ['name', 'designation', 'is_active', 'order', 'image_preview', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'designation', 'bio']
    list_editable = ['order', 'is_active']
    readonly_fields = ['image_preview']
    ordering = ['order', 'name']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['question', 'answer']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'question']

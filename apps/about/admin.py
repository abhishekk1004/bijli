from django.contrib import admin
from apps.about.models import About, Milestone, Stat, TeamMember, FAQ


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description', 'content']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ['year', 'title', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['year', 'title', 'description']
    ordering = ['order', 'year']


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ['number', 'label', 'icon', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['number', 'label']
    ordering = ['order', 'label']


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'designation', 'bio']
    ordering = ['order', 'name']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['question', 'answer']
    ordering = ['order', 'question']

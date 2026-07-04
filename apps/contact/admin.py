from django.contrib import admin
from apps.contact.models import BranchOffice, Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'phone', 'subject', 'message']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'service_interest', 'product_interest', 'created_at']
    ordering = ['-created_at']

    def has_add_permission(self, request):
        return False

    @admin.action(description='Mark selected as read')
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    actions = ['mark_as_read']


@admin.register(BranchOffice)
class BranchOfficeAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'is_head_office', 'is_active', 'order']
    list_filter = ['is_active', 'is_head_office']
    search_fields = ['name', 'address']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'name']

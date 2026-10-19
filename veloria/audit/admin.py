from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'username', 'action', 'ip_address', 'description']
    list_filter = ['action']
    search_fields = ['username', 'description']
    readonly_fields = ['id', 'timestamp', 'user', 'username', 'action', 'ip_address', 'user_agent', 'description']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

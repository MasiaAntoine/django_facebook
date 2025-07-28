from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['utilisateur', 'emetteur', 'type', 'message_court', 'lu', 'date']
    list_filter = ['type', 'lu', 'date']
    search_fields = ['utilisateur__username', 'emetteur__username', 'message']
    ordering = ['-date']
    readonly_fields = ['date']
    
    def message_court(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    message_court.short_description = 'Message'
    
    fieldsets = (
        ('Participants', {'fields': ('utilisateur', 'emetteur')}),
        ('Notification', {'fields': ('type', 'message', 'lu')}),
        ('Métadonnées', {'fields': ('date',)}),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('utilisateur', 'emetteur')

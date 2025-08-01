from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['utilisateur', 'emetteur', 'type', 'lu', 'date']
    list_filter = ['type', 'lu', 'date']
    search_fields = ['utilisateur__username', 'emetteur__username']
    ordering = ['-date']
    readonly_fields = ['date']
    
    fieldsets = (
        ('Participants', {'fields': ('utilisateur', 'emetteur')}),
        ('Notification', {'fields': ('type', 'lu')}),
        ('Métadonnées', {'fields': ('date',)}),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('utilisateur', 'emetteur')

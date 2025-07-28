from django.contrib import admin
from .models import Ami


@admin.register(Ami)
class AmiAdmin(admin.ModelAdmin):
    list_display = ['demandeur', 'receveur', 'accepter', 'bloquer', 'created_at']
    list_filter = ['accepter', 'bloquer', 'created_at']
    search_fields = ['demandeur__username', 'receveur__username']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Relation d\'amitié', {'fields': ('demandeur', 'receveur')}),
        ('Statut', {'fields': ('accepter', 'bloquer')}),
        ('Métadonnées', {'fields': ('created_at',)}),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('demandeur', 'receveur')

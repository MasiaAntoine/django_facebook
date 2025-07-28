from django.contrib import admin
from .models import Reaction, Commentaire, Partage


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'type', 'created_at']
    list_filter = ['type', 'created_at']
    search_fields = ['user__username', 'post__title']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'post')


@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'contenu_court', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__title', 'contenu']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    def contenu_court(self, obj):
        return obj.contenu[:50] + "..." if len(obj.contenu) > 50 else obj.contenu
    contenu_court.short_description = 'Contenu'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'post')


@admin.register(Partage)
class PartageAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__title']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'post')

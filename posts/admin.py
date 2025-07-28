from django.contrib import admin
from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'category', 'is_story', 'created_at']
    list_filter = ['is_story', 'category', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    fieldsets = (
        (None, {'fields': ('title', 'description', 'user')}),
        ('Catégorisation', {'fields': ('category', 'is_story')}),
        ('Média', {'fields': ('photos',)}),
        ('Métadonnées', {'fields': ('created_at',)}),
    )

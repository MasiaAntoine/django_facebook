from django.contrib import admin
from .models import UtilisateurPersonnaliser


@admin.register(UtilisateurPersonnaliser)
class UtilisateurPersonnaliserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'telephone', 'ville', 'est_privee', 'date_joined', 'is_active']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'est_privee', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'telephone', 'ville']
    ordering = ['-date_joined']
    readonly_fields = ['date_joined', 'last_login']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email', 'telephone', 'ville', 'photo_profil')}),
        ('Paramètres de confidentialité', {'fields': ('est_privee',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )

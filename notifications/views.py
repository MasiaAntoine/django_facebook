from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import ListView
from django.views import View
from .models import Notification


class ListeNotificationsView(LoginRequiredMixin, ListView):
    """Affiche la liste des notifications de l'utilisateur"""
    model = Notification
    template_name = 'notifications/liste.html'
    context_object_name = 'notifications'
    
    def get_queryset(self):
        """Retourne les notifications de l'utilisateur connecté"""
        queryset = Notification.objects.filter(utilisateur=self.request.user).order_by('-date')
        queryset.filter(lu=False).update(lu=True)
        return queryset


class MarquerCommeLueView(LoginRequiredMixin, View):
    """Marque une notification comme lue"""
    
    def post(self, request, notification_id):
        try:
            notification = get_object_or_404(
                Notification, 
                id=notification_id, 
                utilisateur=request.user
            )
            notification.lu = True
            notification.save()
            return JsonResponse({'success': True})
        except Notification.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Notification non trouvée'})


class CompterNonLuesView(LoginRequiredMixin, View):
    """Retourne le nombre de notifications non lues"""
    
    def get(self, request):
        count = Notification.objects.filter(utilisateur=request.user, lu=False).count()
        return JsonResponse({'count': count})

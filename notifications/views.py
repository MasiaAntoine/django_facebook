from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Notification


@login_required
def liste_notifications(request):
    """Affiche la liste des notifications de l'utilisateur"""
    notifications = Notification.objects.filter(utilisateur=request.user).order_by('-date')
    
    notifications.filter(lu=False).update(lu=True)
    
    return render(request, 'notifications/liste.html', {
        'notifications': notifications
    })


@login_required
def marquer_comme_lue(request, notification_id):
    """Marque une notification comme lue"""
    try:
        notification = Notification.objects.get(id=notification_id, utilisateur=request.user)
        notification.lu = True
        notification.save()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification non trouvée'})


@login_required
def compter_non_lues(request):
    """Retourne le nombre de notifications non lues"""
    count = Notification.objects.filter(utilisateur=request.user, lu=False).count()
    return JsonResponse({'count': count})

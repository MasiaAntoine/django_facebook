from django.shortcuts import render
from django.db.models import Q
from utilisateurs.models import UtilisateurPersonnaliser

def rechercher_amis(request):
    query = request.GET.get('q', '')
    utilisateurs = []
    
    if query:
        utilisateurs = UtilisateurPersonnaliser.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        ).exclude(id=request.user.id if request.user.is_authenticated else None)
    
    context = {
        'utilisateurs': utilisateurs,
        'query': query
    }
    return render(request, 'amis/rechercher.html', context)

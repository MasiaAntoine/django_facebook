from django.shortcuts import render
from django.db.models import Q
from django.template.loader import render_to_string

from utilisateurs.models import UtilisateurPersonnaliser

def rechercher_amis(request):
    query = request.GET.get('q', '')
    utilisateurs = []
    modal_body_search = render_to_string("components/modal_search_body.html", request=request)
    if query:
        utilisateurs = UtilisateurPersonnaliser.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(ville__icontains=query)
        ).exclude(id=request.user.id if request.user.is_authenticated else None)
    
    context = {
        'utilisateurs': utilisateurs,
        'query': query,
	    'modal_body_search': modal_body_search,
    }
    return render(request, 'amis/rechercher.html', context)

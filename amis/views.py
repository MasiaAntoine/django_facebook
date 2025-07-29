from django.shortcuts import render
from django.db.models import Q
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from utilisateurs.models import UtilisateurPersonnaliser


class RechercherAmisView(TemplateView):
    template_name = 'amis/rechercher.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        utilisateurs = []
        modal_body_search = render_to_string("components/modal_search_body.html", request=self.request)
        
        if query:
            utilisateurs = UtilisateurPersonnaliser.objects.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(ville__icontains=query)
            ).exclude(id=self.request.user.id if self.request.user.is_authenticated else None)
        
        context.update({
            'utilisateurs': utilisateurs,
            'query': query,
            'modal_body_search': modal_body_search,
        })
        return context

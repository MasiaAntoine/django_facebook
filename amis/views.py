from django.shortcuts import render
from django.db.models import Q
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from utilisateurs.models import UtilisateurPersonnaliser


class RechercherAmisView(TemplateView):
    template_name = 'amis/rechercher.html'
    
    def get_context_data(self, **kwargs):
        import unicodedata
        def strip_accents(s):
            return ''.join(c for c in unicodedata.normalize('NFD', s or '') if unicodedata.category(c) != 'Mn').lower()

        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        utilisateurs = []
        modal_body_search = render_to_string("components/modal_search_body.html", request=self.request)

        if query:
            utilisateurs_qs = UtilisateurPersonnaliser.objects.all().exclude(id=self.request.user.id if self.request.user.is_authenticated else None)
            query_norm = strip_accents(query)
            utilisateurs = [u for u in utilisateurs_qs if (
                query_norm in strip_accents(u.first_name)
                or query_norm in strip_accents(u.last_name)
                or query_norm in strip_accents(u.ville)
            )]

        context.update({
            'utilisateurs': utilisateurs,
            'query': query,
            'modal_body_search': modal_body_search,
        })
        return context

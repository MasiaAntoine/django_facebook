from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, get_object_or_404, render
from utilisateurs.models import UtilisateurPersonnaliser
from .models import Ami
from notifications.models import Notification
from django.db.models import Q
from django.template.loader import render_to_string
from django.views.generic import TemplateView



class AmisActionsView(TemplateView):
    def post(self, request, *args, **kwargs):
        action = kwargs.get('action')
        user_id = kwargs.get('user_id')
        if action == 'ajouter':
            return self.ajouter_ami(request, user_id)
        elif action == 'supprimer':
            return self.supprimer_ami(request, user_id)
        elif action == 'accepter':
            return self.accepter_ami(request, user_id)
        else:
            return redirect('home')

    def ajouter_ami(self, request, user_id):
        receveur = get_object_or_404(UtilisateurPersonnaliser, id=user_id)
        demandeur = request.user
        if demandeur == receveur:
            return redirect('profil')
        relation, created = Ami.objects.get_or_create(demandeur=demandeur, receveur=receveur)
        if created:
            Notification.creer_notification(
                utilisateur=receveur,
                emetteur=demandeur,
                type_notif='friend_request',
                message=f"vous a envoyé une demande d'ami."
            )
        return redirect('profil_user', user_id=receveur.id)

    def supprimer_ami(self, request, user_id):
        autre_utilisateur = get_object_or_404(UtilisateurPersonnaliser, id=user_id)
        utilisateur = request.user
        Ami.objects.filter(
            (Q(demandeur=utilisateur, receveur=autre_utilisateur) |
             Q(demandeur=autre_utilisateur, receveur=utilisateur))
        ).delete()
        return redirect('profil_user', user_id=autre_utilisateur.id)

    def accepter_ami(self, request, user_id):
        autre_utilisateur = get_object_or_404(UtilisateurPersonnaliser, id=user_id)
        utilisateur = request.user
        relation = Ami.objects.filter(
            demandeur=autre_utilisateur,
            receveur=utilisateur,
            accepter=False
        ).first()
        if relation:
            relation.accepter = True
            relation.save()
            Notification.creer_notification(
                utilisateur=autre_utilisateur,
                emetteur=utilisateur,
                type_notif='friend_accept',
                message=f"a accepté votre demande d'ami."
            )
        return redirect('profil_user', user_id=autre_utilisateur.id)


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

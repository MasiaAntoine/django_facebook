from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from posts.views import ListingMyPostsView
from utilisateurs.forms import InscriptionForm, ConnexionForm, ProfilForm, CustomPasswordChangeForm
from amis.models import Ami
from django.db.models import Q


class InscriptionView(FormView):
	template_name = 'utilisateurs/inscription.html'
	form_class = InscriptionForm
	success_url = reverse_lazy('home')

	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		return super().form_valid(form)


class ConnexionView(FormView):
	template_name = 'utilisateurs/connexion.html'
	form_class = ConnexionForm
	success_url = reverse_lazy('home')

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		if self.request.method == 'POST':
			kwargs['data'] = self.request.POST
		return kwargs

	def form_valid(self, form):
		user = form.get_user()
		login(self.request, user)
		return super().form_valid(form)


class DeconnexionView(View):
	def get(self, request):
		logout(request)
		return redirect('connexion')

	def post(self, request):
		logout(request)
		return redirect('connexion')


@method_decorator(csrf_protect, name='dispatch')
class SupprimerCompteView(LoginRequiredMixin, TemplateView):
	template_name = 'utilisateurs/supprimer_compte.html'
	login_url = reverse_lazy('connexion')

	def post(self, request):
		user = request.user
		logout(request)
		user.delete()
		messages.success(request, "Votre compte a bien été supprimé.")
		return redirect('connexion')


class MonCompteView(LoginRequiredMixin, TemplateView):
	template_name = 'utilisateurs/mon_compte.html'
	login_url = reverse_lazy('connexion')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = self.request.user
		context['profil_form'] = ProfilForm(instance=user)
		context['password_form'] = CustomPasswordChangeForm(user)
		return context

	def post(self, request):
		user = request.user

		if 'update_profil' in request.POST:
			profil_form = ProfilForm(request.POST, request.FILES, instance=user)
			if profil_form.is_valid():
				profil_form.save()
				messages.success(request, "Profil mis à jour avec succès.")
				return redirect('mon_compte')
			else:
				password_form = CustomPasswordChangeForm(user)
				return render(request, self.template_name, {
					'profil_form': profil_form,
					'password_form': password_form
				})

		elif 'update_password' in request.POST:
			password_form = CustomPasswordChangeForm(user, request.POST)
			if password_form.is_valid():
				user = password_form.save()
				update_session_auth_hash(request, user)
				messages.success(request, "Mot de passe modifié avec succès.")
				return redirect('mon_compte')
			else:
				profil_form = ProfilForm(instance=user)
				return render(request, self.template_name, {
					'profil_form': profil_form,
					'password_form': password_form
				})

		return redirect('mon_compte')


class ProfilView(LoginRequiredMixin, TemplateView):
	template_name = 'utilisateurs/profil.html'
	login_url = reverse_lazy('connexion')

	def get(self, request, *args, **kwargs):
		user_id = kwargs.get('user_id')
		if user_id and user_id == request.user.id:
			from django.shortcuts import redirect
			return redirect('profil')
		if user_id:
			from django.contrib.auth import get_user_model
			from django.shortcuts import redirect
			try:
				user_profil = get_user_model().objects.get(id=user_id)
			except get_user_model().DoesNotExist:
				return redirect('home')
			# Vérifier si l'utilisateur courant est bloqué par user_profil
			if Ami.is_blocked(request.user, user_profil):
				self.only_block_message = True
				self.blocked_by = user_profil
				return super().get(request, *args, **kwargs)
		return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		from posts.models import Post
		from django.contrib.auth import get_user_model
		from amis.models import Ami
		from interactions.models import Reaction
		from django.db.models import Q, Count
		from django.template.loader import render_to_string

		context = super().get_context_data(**kwargs)
		user_id = kwargs.get('user_id')

		if user_id:
			user_profil = get_user_model().objects.get(id=user_id)
			is_own_profile = False
		else:
			user_profil = self.request.user
			is_own_profile = True

		# Si l'utilisateur courant est bloqué par user_profil, afficher uniquement le message
		if hasattr(self, 'only_block_message') and getattr(self, 'only_block_message', False):
			context['blocked_by'] = self.blocked_by
			context['only_block_message'] = True
			return context

		context['user_profil'] = user_profil
		context['is_own_profile'] = is_own_profile

		# Statistiques publiques
		total_posts = Post.objects.filter(user=user_profil).count()
		context['user_stats'] = {
			'total_posts': total_posts,
			'member_since': user_profil.date_joined,
		}

		# Amis
		amis_relations = Ami.objects.filter(
			Q(demandeur=user_profil, accepter=True) |
			Q(receveur=user_profil, accepter=True)
		).select_related('demandeur', 'receveur')

		amis = []
		amis_ids = set()
		for relation in amis_relations:
			ami = relation.receveur if relation.demandeur == user_profil else relation.demandeur
			if ami.id not in amis_ids:
				amis_ids.add(ami.id)
				ami.amis_communs = 0
				if not is_own_profile:
					ami.amis_communs = Ami.objects.filter(
						Q(demandeur=self.request.user, receveur=ami, accepter=True) |
						Q(demandeur=ami, receveur=self.request.user, accepter=True)
					).count()
				amis.append(ami)
		context['amis'] = amis

		# Statuts ami/bloqué
		est_bloque = Ami.objects.filter(
			demandeur=self.request.user,
			receveur=user_profil,
			bloquer=True
		).exists() if not is_own_profile else False

		est_bloque_par = Ami.objects.filter(
			demandeur=user_profil,
			receveur=self.request.user,
			bloquer=True
		).exists() if not is_own_profile else False

		context['est_bloque'] = est_bloque
		context['est_bloque_par'] = est_bloque_par

		est_ami = False
		demande_envoyee = False
		demande_recue = False
		if not is_own_profile and not est_bloque and not est_bloque_par:
			est_ami = Ami.objects.filter(
				(Q(demandeur=self.request.user, receveur=user_profil) |
				 Q(demandeur=user_profil, receveur=self.request.user)) &
				Q(accepter=True)
			).exists()
			demande_envoyee = Ami.objects.filter(
				demandeur=self.request.user,
				receveur=user_profil,
				accepter=False
			).exists()
			demande_recue = Ami.objects.filter(
				demandeur=user_profil,
				receveur=self.request.user,
				accepter=False
			).exists()

		context['est_ami'] = est_ami
		context['demande_envoyee'] = demande_envoyee
		context['demande_recue'] = demande_recue

		# Posts & Réactions
		if not user_profil.est_privee or is_own_profile:
			user_posts = Post.objects.filter(user=user_profil, is_story=False).order_by('-created_at')

			grouped_reactions = (
				Reaction.objects
				.filter(post__in=user_posts)
				.values('post_id', 'type')
				.annotate(total=Count('id'))
			)

			user_reactions = {}
			if self.request.user.is_authenticated:
				user_reactions_qs = Reaction.objects.filter(user=self.request.user, post__in=user_posts)
				user_reactions = {r.post_id: r for r in user_reactions_qs}

			context['posts'] = user_posts
			context['grouped_reactions'] = grouped_reactions
			context['user_reactions'] = user_reactions
			context['reaction_types'] = [
				{'type': 'like', 'emoji': '👍'},
				{'type': 'love', 'emoji': '❤️'},
				{'type': 'happy', 'emoji': '😊'},
				{'type': 'angry', 'emoji': '😠'},
				{'type': 'sad', 'emoji': '😢'},
			]
			context["modal_body_search"] = render_to_string("components/modal_search_body.html", request=self.request)
		else:
			context['posts'] = []

		return context


# --- Vue pour bloquer/débloquer un utilisateur ---
class ActionBloquerView(LoginRequiredMixin, View):
	@method_decorator(csrf_protect)
	def post(self, request, user_id):
		from django.contrib.auth import get_user_model
		User = get_user_model()
		try:
			cible = User.objects.get(id=user_id)
		except User.DoesNotExist:
			return redirect('home')
		if cible == request.user:
			return redirect('profil')

		# On cherche une relation existante
		ami_relation = Ami.objects.filter(
			Q(demandeur=request.user, receveur=cible) | Q(demandeur=cible, receveur=request.user)
		).first()

		if ami_relation and ami_relation.demandeur == request.user and ami_relation.bloquer:
			# Déblocage : on supprime juste le blocage, pas de demande d'ami
			ami_relation.bloquer = False
			ami_relation.save()
			# Supprimer toute demande d'ami non acceptée dans les deux sens
			Ami.objects.filter(
				(
						Q(demandeur=request.user, receveur=cible) |
						Q(demandeur=cible, receveur=request.user)
				) & Q(accepter=False)
			).delete()
		else:
			# Blocage : on supprime toute relation d'amitié (acceptée ou non)
			Ami.objects.filter(
				Q(demandeur=request.user, receveur=cible) | Q(demandeur=cible, receveur=request.user)
			).delete()
			# On crée une relation de blocage
			Ami.objects.create(demandeur=request.user, receveur=cible, bloquer=True)

		messages.success(request, "Action de blocage/déblocage effectuée.")
		return redirect('profil_user', user_id=cible.id)

from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from utilisateurs.forms import InscriptionForm, ConnexionForm, ProfilForm, CustomPasswordChangeForm


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
		# Récupérer l'ID de l'utilisateur depuis l'URL (optionnel)
		user_id = kwargs.get('user_id')
		
		# Si on accède à son propre profil avec un ID, rediriger vers la page sans ID
		if user_id and user_id == request.user.id:
			from django.shortcuts import redirect
			return redirect('profil')
		
		# Si un ID est fourni, vérifier que l'utilisateur existe
		if user_id:
			from django.contrib.auth import get_user_model
			from django.shortcuts import redirect
			try:
				get_user_model().objects.get(id=user_id)
			except get_user_model().DoesNotExist:
				# Si l'utilisateur n'existe pas, rediriger vers la racine
				return redirect('home')
		
		return super().get(request, *args, **kwargs)
	
	def get_context_data(self, **kwargs):
		from posts.models import Post
		from django.contrib.auth import get_user_model
		from amis.models import Ami
		from django.db.models import Q

		context = super().get_context_data(**kwargs)

		# Récupérer l'ID de l'utilisateur depuis l'URL (optionnel)
		user_id = kwargs.get('user_id')

		if user_id:
			# Afficher le profil d'un autre utilisateur (existence déjà vérifiée dans get())
			user_profil = get_user_model().objects.get(id=user_id)
			is_own_profile = False
		else:
			# Afficher son propre profil
			user_profil = self.request.user
			is_own_profile = True

		context['user_profil'] = user_profil
		context['is_own_profile'] = is_own_profile

		# Calculer les statistiques publiques (toujours visibles)
		total_posts = Post.objects.filter(user=user_profil).count()
		context['user_stats'] = {
			'total_posts': total_posts,
			'member_since': user_profil.date_joined,
		}

		# Récupérer les amis de l'utilisateur
		amis_relations = Ami.objects.filter(
			Q(demandeur=user_profil, accepter=True) |
			Q(receveur=user_profil, accepter=True)
		).select_related('demandeur', 'receveur')

		# Extraire les utilisateurs amis (en excluant l'utilisateur lui-même)
		amis = []
		amis_ids = set()  # Pour éviter les doublons
		
		for relation in amis_relations:
			if relation.demandeur == user_profil:
				ami = relation.receveur
			else:
				ami = relation.demandeur
			
			# Éviter les doublons
			if ami.id not in amis_ids:
				amis_ids.add(ami.id)
				
				# Calculer les amis en commun si c'est le profil d'un autre utilisateur
				if not is_own_profile:
					amis_communs = Ami.objects.filter(
						Q(demandeur=self.request.user, receveur=ami, accepter=True) |
						Q(demandeur=ami, receveur=self.request.user, accepter=True)
					).count()
					ami.amis_communs = amis_communs
				else:
					ami.amis_communs = 0
				
				amis.append(ami)

		context['amis'] = amis

		# Si ce n'est pas un profil privé OU si c'est son propre profil, afficher les posts
		if not user_profil.est_privee or is_own_profile:
			context['user_posts'] = Post.objects.filter(user=user_profil).order_by('-created_at')
		else:
			context['user_posts'] = []

		return context

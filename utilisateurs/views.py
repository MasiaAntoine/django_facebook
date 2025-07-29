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

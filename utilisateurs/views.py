from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from utilisateurs.forms import InscriptionForm, ConnexionForm, ProfilForm, CustomPasswordChangeForm


def inscription_view(request):
	if request.method == 'POST':
		form = InscriptionForm(request.POST, request.FILES)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('home')  # redirige vers le fil d’actu ou autre
	else:
		form = InscriptionForm()
	return render(request, 'utilisateurs/inscription.html', {'form': form})


def connexion_view(request):
	if request.method == 'POST':
		form = ConnexionForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect('home')
	else:
		form = ConnexionForm()
	return render(request, 'utilisateurs/connexion.html', {'form': form})


def deconnexion_view(request):
	logout(request)
	return redirect('connexion')


@login_required
@csrf_protect
def supprimer_compte_view(request):
	if request.method == 'POST':
		user = request.user
		logout(request)
		user.delete()
		messages.success(request, "Votre compte a bien été supprimé.")
		return redirect('connexion')
	return render(request, 'utilisateurs/supprimer_compte.html')


@login_required
def mon_compte_view(request):
	user = request.user
	profil_form = ProfilForm(instance=user)
	password_form = CustomPasswordChangeForm(user)

	if request.method == 'POST':
		if 'update_profil' in request.POST:
			profil_form = ProfilForm(request.POST, request.FILES, instance=user)
			if profil_form.is_valid():
				profil_form.save()
				messages.success(request, "Profil mis à jour avec succès.")
				return redirect('mon_compte')

		elif 'update_password' in request.POST:
			password_form = CustomPasswordChangeForm(user, request.POST)
			if password_form.is_valid():
				user = password_form.save()
				update_session_auth_hash(request, user)
				messages.success(request, "Mot de passe modifié avec succès.")
				return redirect('mon_compte')

	return render(request, 'utilisateurs/mon_compte.html', {
		'profil_form': profil_form,
		'password_form': password_form
	})

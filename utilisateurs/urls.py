# utilisateurs/urls.py
from django.urls import path
from .views import InscriptionView, ConnexionView, DeconnexionView, SupprimerCompteView, MonCompteView, ProfilView, ActionBloquerView

urlpatterns = [
	path('inscription/', InscriptionView.as_view(), name='inscription'),
	path('connexion/', ConnexionView.as_view(), name='connexion'),
	path('deconnexion/', DeconnexionView.as_view(), name='deconnexion'),
	path('supprimer/', SupprimerCompteView.as_view(), name='supprimer_compte'),
	path('mon_compte/', MonCompteView.as_view(), name='mon_compte'),
	path('profil/', ProfilView.as_view(), name='profil'),
	path('profil/<int:user_id>/', ProfilView.as_view(), name='profil_user'),
	path('profil/<int:user_id>/bloquer/', ActionBloquerView.as_view(), name='bloquer_user'),
]

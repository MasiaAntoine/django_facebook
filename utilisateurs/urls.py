# utilisateurs/urls.py
from django.urls import path
from .views import inscription_view, connexion_view, deconnexion_view, supprimer_compte_view, mon_compte_view

urlpatterns = [
	path('inscription/', inscription_view, name='inscription'),
	path('connexion/', connexion_view, name='connexion'),
	path('deconnexion/', deconnexion_view, name='deconnexion'),
	path('supprimer/', supprimer_compte_view, name='supprimer_compte'),
	path('mon_compte/', mon_compte_view, name='mon_compte'),
]

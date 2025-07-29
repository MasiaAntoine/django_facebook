from django.urls import path
from . import views
from .views import CommentaireCreateView, ReactionCreateView

app_name = 'interactions'

urlpatterns = [
	path('commentaire/', CommentaireCreateView.as_view(), name='ajout_commentaire'),
	path('reaction/', ReactionCreateView.as_view(), name='ajout_reaction'),
]

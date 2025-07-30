
from django.urls import path
from .views import RechercherAmisView, AmisActionsView


app_name = 'amis'

urlpatterns = [
    path('rechercher/', RechercherAmisView.as_view(), name='rechercher_amis'),
    path('<str:action>/<int:user_id>/', AmisActionsView.as_view(), name='action_ami'),
]

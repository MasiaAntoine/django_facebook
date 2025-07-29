from django.urls import path
from .views import RechercherAmisView

app_name = 'amis'

urlpatterns = [
    path('rechercher/', RechercherAmisView.as_view(), name='rechercher_amis'),
]

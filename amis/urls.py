from django.urls import path
from . import views

app_name = 'amis'

urlpatterns = [
    path('rechercher/', views.rechercher_amis, name='rechercher_amis'),
]

from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.ListeNotificationsView.as_view(), name='liste'),
    path('marquer-lue/<int:notification_id>/', views.MarquerCommeLueView.as_view(), name='marquer_lue'),
    path('api/count/', views.CompterNonLuesView.as_view(), name='compter_non_lues'),
]

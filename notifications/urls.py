from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.liste_notifications, name='liste'),
    path('marquer-lue/<int:notification_id>/', views.marquer_comme_lue, name='marquer_lue'),
    path('api/count/', views.compter_non_lues, name='compter_non_lues'),
]

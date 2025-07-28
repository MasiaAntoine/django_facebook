from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('utilisateurs/', include('utilisateurs.urls')),
    path('amis/', include('amis.urls')),
    path('posts/', include('posts.urls')),
    path('interactions/', include('interactions.urls')),
    path('notifications/', include('notifications.urls')),
]

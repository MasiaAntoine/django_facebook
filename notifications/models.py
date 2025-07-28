from django.db import models

from django_facebook import settings


class Notification(models.Model):
	NOTIF_TYPES = [
		('like', 'Like'),
		('comment', 'Commentaire'),
		('friend_request', 'Demande d’ami'),
		('share', 'Partage'),
	]

	utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
	emetteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='emissions')
	type = models.CharField(max_length=50, choices=NOTIF_TYPES)
	message = models.TextField()
	lu = models.BooleanField(default=False)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Notif {self.type} de {self.emetteur} à {self.utilisateur}"

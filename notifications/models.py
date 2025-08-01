from django.db import models

from django_facebook import settings


class Notification(models.Model):
	NOTIF_TYPES = [
		('like', 'Like'),
		('reaction', 'Réaction'),
		('comment', 'Commentaire'),
		('friend_request', 'Demande d’ami'),
		('friend_accept', 'Demande d’ami acceptée'),
		('share', 'Partage'),
	]

	utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
	emetteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='emissions')
	type = models.CharField(max_length=50, choices=NOTIF_TYPES)
	lu = models.BooleanField(default=False)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Notif {self.type} de {self.emetteur} à {self.utilisateur}"

	@classmethod
	def creer_notification(cls, utilisateur, emetteur, type_notif):
		"""Méthode utilitaire pour créer une notification"""
		if utilisateur != emetteur:
			return cls.objects.create(
				utilisateur=utilisateur,
				emetteur=emetteur,
				type=type_notif,
			)
		return None

	class Meta:
		ordering = ['-date']

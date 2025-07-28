from django.db import models

from django_facebook import settings


class Ami(models.Model):
	demandeur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='demandes_envoyees')
	receveur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='demandes_recues')
	accepter = models.BooleanField(default=False)
	bloquer = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('demandeur', 'receveur')

	def __str__(self):
		return f"{self.demandeur} -> {self.receveur}"

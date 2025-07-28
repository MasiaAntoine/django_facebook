from django.contrib.auth.models import AbstractUser
from django.db import models


class UtilisateurPersonnaliser(AbstractUser):
	photo_profil = models.ImageField(upload_to='photos/profils/', null=True, blank=True)
	telephone = models.CharField(max_length=15, null=True, blank=True)

	def __str__(self):
		return self.username

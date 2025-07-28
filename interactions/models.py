from django.db import models

from django_facebook import settings
from posts.models import Post


class Reaction(models.Model):
	REACTION_TYPES = [
		('like', 'Like'),
		('love', 'Love'),
		('happy', 'Happy'),
		('angry', 'Angry'),
		('sad', 'Sad'),
	]
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	type = models.CharField(max_length=20, choices=REACTION_TYPES)
	created_at = models.DateTimeField(auto_now_add=True)


class Commentaire(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	contenu = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)


class Partage(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

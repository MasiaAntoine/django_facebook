from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from interactions.models import Commentaire, Reaction
from notifications.models import Notification
from posts.models import Post


class CommentaireCreateView(LoginRequiredMixin, CreateView):
	model = Commentaire
	login_url = '/utilisateurs/connexion/'
	fields = ['contenu']
	http_method_names = ['post']

	def form_valid(self, form):
		post_id = self.request.POST.get("post_id")
		post = Post.objects.get(id=post_id)
		form.instance.post = post
		form.instance.user = self.request.user
		response = super().form_valid(form)
		if post.user != self.request.user:
			Notification.creer_notification(
				utilisateur=post.user,
				emetteur=self.request.user,
				type_notif='comment',
			)
		return response

	def get_success_url(self):
		return self.request.META.get("HTTP_REFERER", reverse_lazy('posts:all_posts'))


class ReactionCreateView(LoginRequiredMixin, CreateView):
	model = Reaction
	login_url = '/utilisateurs/connexion/'
	fields = ['type']
	http_method_names = ['post']

	def form_valid(self, form):
		post_id = self.request.POST.get("post_id")
		post = Post.objects.get(id=post_id)
		form.instance.post = post
		form.instance.user = self.request.user
		response = super().form_valid(form)
		if post.user != self.request.user:
			Notification.creer_notification(
				utilisateur=post.user,
				emetteur=self.request.user,
				type_notif='like',
			)
		return response

	def get_success_url(self):
		return self.request.META.get("HTTP_REFERER", reverse_lazy('posts:all_posts'))

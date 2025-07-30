from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from interactions.models import Commentaire, Reaction
from posts.models import Post


class CommentaireCreateView(LoginRequiredMixin, CreateView):
	model = Commentaire
	login_url = '/utilisateurs/connexion/'
	fields = ['contenu']
	http_method_names = ['post']

	def form_valid(self, form):
		post_id = self.request.POST.get("post_id")
		form.instance.post = Post.objects.get(id=post_id)
		form.instance.user = self.request.user
		return super().form_valid(form)

	def get_success_url(self):
		return self.request.META.get("HTTP_REFERER", reverse_lazy('posts:all_posts'))


class ReactionCreateView(LoginRequiredMixin, CreateView):
	model = Reaction
	login_url = '/utilisateurs/connexion/'
	fields = ['type']
	http_method_names = ['post']

	def form_valid(self, form):
		post_id = self.request.POST.get("post_id")
		form.instance.post = Post.objects.get(id=post_id)
		form.instance.user = self.request.user
		return super().form_valid(form)

	def get_success_url(self):
		return self.request.META.get("HTTP_REFERER", reverse_lazy('posts:all_posts'))

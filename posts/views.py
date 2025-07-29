from django.db.models import Count
from django.views.generic import ListView

from interactions.models import Reaction
from posts.models import Post


class ListingAllPostsView(ListView):
	model = Post
	template_name = "posts/allPosts.html"
	context_object_name = "posts"

	def get_queryset(self):
		return Post.objects.filter(is_story=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		# Ajoute les types de réactions avec emojis
		context['reaction_types'] = [
			{'type': 'like', 'emoji': '👍'},
			{'type': 'love', 'emoji': '❤️'},
			{'type': 'happy', 'emoji': '😊'},
			{'type': 'angry', 'emoji': '😠'},
			{'type': 'sad', 'emoji': '😢'},
		]

		# Regroupement des réactions (supposé que tu as déjà cela)
		from django.db.models import Count
		from interactions.models import Reaction
		grouped = (
			Reaction.objects
			.values('post_id', 'type')
			.annotate(total=Count('id'))
		)
		context['grouped_reactions'] = grouped

		return context

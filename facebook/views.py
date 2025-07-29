from django.db.models import Count
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from interactions.models import Reaction
from posts.models import Post


class HomeView(TemplateView):
	template_name = "facebook/home.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		modal_body_search = render_to_string("components/modal_search_body.html", request=self.request)
		posts = Post.objects.filter(is_story=False)

		grouped_reactions = (
			Reaction.objects
			.filter(post__in=posts)
			.values('post_id', 'type')
			.annotate(total=Count('id'))
		)

		context.update({
			"modal_body_search": modal_body_search,
			"posts": posts,
			"grouped_reactions": grouped_reactions,
			"reaction_types": [
				{'type': 'like', 'emoji': '👍'},
				{'type': 'love', 'emoji': '❤️'},
				{'type': 'happy', 'emoji': '😊'},
				{'type': 'angry', 'emoji': '😠'},
				{'type': 'sad', 'emoji': '😢'},
			],
		})
		return context

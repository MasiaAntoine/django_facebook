from django.db.models import Count, Prefetch
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, CreateView

from interactions.models import Reaction
from posts.models import Post, PostImage
from posts.forms import PostForm


class BasePostListView(ListView):
	model = Post
	template_name = "posts/allPosts.html"
	context_object_name = "posts"
	filter_by_user_id = None  # Peut être défini dynamiquement

	def get_queryset(self):
		qs = Post.objects.filter(is_story=False).prefetch_related(
			Prefetch('images', queryset=PostImage.objects.all())
		).order_by('-created_at')

		user_id = self.kwargs.get('user_id') or self.filter_by_user_id
		if user_id:
			qs = qs.filter(user__id=user_id)

		return qs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		posts = context['posts']

		grouped_reactions = (
			Reaction.objects
			.filter(post__in=posts)
			.values('post_id', 'type')
			.annotate(total=Count('id'))
		)

		user_reactions = {}
		if self.request.user.is_authenticated:
			user_reactions_qs = Reaction.objects.filter(user=self.request.user, post__in=posts)
			user_reactions = {r.post_id: r for r in user_reactions_qs}

		context.update({
			"modal_body_search": render_to_string("components/modal_search_body.html", request=self.request),
			"grouped_reactions": grouped_reactions,
			"reaction_types": [
				{'type': 'like', 'emoji': '👍'},
				{'type': 'love', 'emoji': '❤️'},
				{'type': 'happy', 'emoji': '😊'},
				{'type': 'angry', 'emoji': '😠'},
				{'type': 'sad', 'emoji': '😢'},
			],
			"user_reactions": user_reactions,
		})
		return context


class ListingAllPostsView(BasePostListView):
	filter_by_user = False  # Affiche tous les posts


class ListingMyPostsView(BasePostListView):
	def get_queryset(self):
		user_id = self.kwargs.get("user_id") if hasattr(self, 'kwargs') else self.request.GET.get("user_id")
		self.filter_by_user_id = user_id
		return super().get_queryset()


class CreatePostView(CreateView):
	model = Post
	form_class = PostForm
	template_name = 'components/modal_add_posts.html'
	success_url = reverse_lazy('home')

	def form_valid(self, form):
		post = form.save(commit=False)
		post.user = self.request.user
		post.save()

		files = self.request.FILES.getlist('images')
		for f in files:
			PostImage.objects.create(post=post, image=f)

		return super().form_valid(form)

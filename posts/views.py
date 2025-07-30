from django.db.models import Count
from django.template.loader import render_to_string
from django.views.generic import ListView

from interactions.models import Reaction
from posts.models import Post


class BasePostListView(ListView):
    model = Post
    template_name = "posts/allPosts.html"
    context_object_name = "posts"
    filter_by_user = None  # Par défaut : pas de filtrage utilisateur

    def get_queryset(self):
        qs = Post.objects.filter(is_story=False)
        if self.filter_by_user:
            qs = qs.filter(user=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = context['posts']  # récupère le queryset filtré

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
    filter_by_user = True  # Affiche uniquement mes posts

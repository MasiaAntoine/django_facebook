from django.template.loader import render_to_string
from django.views.generic import TemplateView

from posts.forms import PostForm
from posts.views import ListingAllPostsView

from posts.views import StoryListView


from posts.views import StoryListView

class HomeView(TemplateView):
    template_name = "facebook/home.html"

    def get_context_data(self, **kwargs):
        # Récupération des posts
        listing_view = ListingAllPostsView()
        listing_view.request = self.request
        listing_view.kwargs = {}
        listing_view.object_list = listing_view.get_queryset()

        context = listing_view.get_context_data(**kwargs)

        # Récupération des stories
        story_view = StoryListView()
        story_view.request = self.request
        story_view.kwargs = {}
        story_view.object_list = story_view.get_queryset()

        stories_context = story_view.get_context_data()

        # Merge des contextes
        context.update({
            'modal_body_search': render_to_string("components/modal_search_body.html", request=self.request),
            'form': PostForm(),
            'posts': listing_view.object_list,
            'users_with_story': stories_context['users_with_story'],
        })
        return context

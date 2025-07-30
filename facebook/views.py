from django.template.loader import render_to_string
from django.views.generic import TemplateView
from posts.views import ListingAllPostsView


class HomeView(TemplateView):
	template_name = "facebook/home.html"

	def get_context_data(self, **kwargs):
		listing_view = ListingAllPostsView()
		listing_view.request = self.request
		listing_view.kwargs = {}
		listing_view.object_list = listing_view.get_queryset()

		context = listing_view.get_context_data(**kwargs)
		context['modal_body_search'] = render_to_string("components/modal_search_body.html", request=self.request)
		return context

from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from posts.models import Post


class HomeView(TemplateView):
	template_name = "facebook/home.html"
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		modal_body_search = render_to_string("components/modal_search_body.html", request=self.request)
		posts = Post.objects.filter(is_story=False)
		
		context.update({
			"modal_body_search": modal_body_search,
			"posts": posts,
		})
		return context

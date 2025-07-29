from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string

from posts.models import Post


def home(request):
	modal_body_search = render_to_string("components/modal_search_body.html", request=request)
	posts = Post.objects.filter(is_story=False)
	return render(request, "facebook/home.html", {
		"modal_body_search": modal_body_search,
		"posts": posts,
	})

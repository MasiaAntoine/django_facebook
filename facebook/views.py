from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string


def home(request):
	modal_body_search = render_to_string("components/modal_search_body.html", request=request)

	return render(request, "facebook/home.html", {
		"modal_body_search": modal_body_search,
	})

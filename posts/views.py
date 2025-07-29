from django.shortcuts import render
from django.views.generic import ListView

from posts.models import Post


class ListingAllPostsView(ListView):
    model = Post
    template_name = "posts/allPosts.html"
    context_object_name = "posts"
    
    def get_queryset(self):
        return Post.objects.filter(is_story=False)  # filtrage ici
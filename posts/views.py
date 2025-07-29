from django.shortcuts import render

from posts.models import Post


def listing_all_posts(request):
    posts = Post.objects.filter(is_story=False)  # filtrage ici
    return render(request, "posts/allPosts.html", {
        "posts": posts,
    })
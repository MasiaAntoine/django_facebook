from django.urls import path
from .views import ListingAllPostsView, CreatePostView, StoryListView, CreateStoryView

app_name = 'posts'

urlpatterns = [
	path('all/', ListingAllPostsView.as_view(), name='listing_all_posts'),
	path('', ListingAllPostsView.as_view(), name='home'),
	path('create/', CreatePostView.as_view(), name='create_post'),
	path('stories/', StoryListView.as_view(), name='stories'),
	path('create-story/', CreateStoryView.as_view(), name='create_story'),
]

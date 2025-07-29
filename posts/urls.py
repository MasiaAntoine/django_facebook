from django.urls import path
from .views import ListingAllPostsView

app_name = 'posts'

urlpatterns = [
	path('all/', ListingAllPostsView.as_view(), name='listing_all_posts'),
	path('', ListingAllPostsView.as_view(), name='home'),
]

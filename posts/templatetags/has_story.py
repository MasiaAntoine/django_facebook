from datetime import timedelta
from django import template
from django.utils.timezone import now
from posts.models import Post

register = template.Library()

@register.simple_tag
def has_active_story(user):
    if not user.is_authenticated:
        return False
    time_limit = now() - timedelta(hours=24)
    return Post.objects.filter(user=user, is_story=True, created_at__gte=time_limit).exists()

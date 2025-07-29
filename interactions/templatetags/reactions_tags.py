# interactions/templatetags/reactions_tags.py

from django import template

register = template.Library()

@register.filter
def count_reactions(grouped_reactions, post_id, react_type):
    # grouped_reactions est un QuerySet ou liste
    # post_id et react_type sont séparés
    for item in grouped_reactions:
        if item['post_id'] == post_id and item['type'] == react_type:
            return item['total']
    return 0

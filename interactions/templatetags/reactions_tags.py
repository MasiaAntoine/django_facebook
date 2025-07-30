from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
	return dictionary.get(key)


@register.simple_tag
def count_reactions(grouped_reactions, post_id, react_type):
	for item in grouped_reactions:
		if item['post_id'] == post_id and item['type'] == react_type:
			return item['total']
	return 0

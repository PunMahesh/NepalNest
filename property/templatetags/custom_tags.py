from django import template

register = template.Library()

@register.filter(name='get_icon')
def get_icon(icons, safety_item_name):
    return icons.get(safety_item_name, '')

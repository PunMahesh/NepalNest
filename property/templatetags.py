from django import template

register = template.Library()

@register.filter
def format_guest_room(value):
    # Replace underscores with spaces and capitalize each word
    return ' '.join(word.capitalize() for word in value.split('_'))
from django import template

register = template.Library()


@register.simple_tag
def get_pill_color(tag, current_tag):
    if tag == current_tag:
        return "primary"
    else:
        return "secondary"

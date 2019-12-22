from django import template

register = template.Library()

@register.filter
def exclude(qs, qs_to_exclude):
    """Tag to exclude a qs from another."""
    return qs.exclude(pk__in=qs_to_exclude.values_list('pk'))
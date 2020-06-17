from django import template
register = template.Library()

@register.simple_tag(name="multiply")
def multiply(priority, functional, *args, **kwargs):
    return priority * functional or 0

from django import template

register = template.Library()

@register.filter(name='dict_get')
def dict_get(dictionary, key):
    return dictionary.get(key)

@register.filter
def make_range(value):
    return range(value)

@register.filter
def subtract(value, arg):
    return value - arg
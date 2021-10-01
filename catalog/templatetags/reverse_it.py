from django import template

register = template.Library()

@register.simple_tag(name="reverse_str")
def myfunc(value):
    return value[::-1]

@register.filter(name="clean_str")
def clean_str(value):
    return value.replace("a", "e")
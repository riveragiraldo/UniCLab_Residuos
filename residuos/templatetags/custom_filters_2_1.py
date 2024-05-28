from django import template
from os.path import basename
from urllib.parse import unquote

register = template.Library()

@register.filter(name='filename')
def filename(value):
    base_name = basename(value)
    return unquote(base_name)


from django import template
import base64

register = template.Library()

@register.filter
def base64_encode(value):
    value_str = str(value)
    value_bytes = value_str.encode('utf-8')
    base64_bytes = base64.b64encode(value_bytes)
    return base64_bytes.decode('utf-8')


@register.filter
def double_base64_encode(value):
    # Primera codificación en base64
    first_encode = base64.urlsafe_b64encode(str(value).encode()).decode()
    # Segunda codificación en base64
    second_encode = base64.urlsafe_b64encode(first_encode.encode()).decode()
    return second_encode
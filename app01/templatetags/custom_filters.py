from django import template

register = template.Library()

@register.filter
def phone_display(phone):
    return phone[:3] + '****' + phone[-4:]
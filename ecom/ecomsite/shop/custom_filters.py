from django import template

register = template.Library()

@register.filter
def percentage(value, total):
    try:
        return "{:.0%}".format(value / total)
    except ZeroDivisionError:
        return "0%"
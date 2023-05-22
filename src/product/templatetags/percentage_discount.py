from django import template
register = template.Library()


@register.filter
def calc_discount(value, arg):
    """
    Calculate percentage discount
    """
    try:
        value = int(value)
        arg = int(arg)
        return value * (arg/100)
    except:
        return ''

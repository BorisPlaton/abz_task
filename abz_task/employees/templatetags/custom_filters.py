from django import template

register = template.Library()


@register.filter(name='range')
def get_range(value):
    """Возвращает итератор до значения value"""

    return range(value)

from django import template

register = template.Library()


@register.simple_tag
def url_parameters(params: dict = None, **kwargs) -> str:
    """
    Возвращает строку вида `?key1=value1&key2=value2`.

    :param params: Словарь, который обновляет позиционные аргументы `kwargs`.
        Необязательный.
    """

    url_params = ''
    if params and kwargs:
        kwargs.update(params)

    params_list = [f'{key}={value}' for key, value in kwargs.items() if value]
    if params_list:
        url_params = '?' + '&'.join(params_list)

    return url_params

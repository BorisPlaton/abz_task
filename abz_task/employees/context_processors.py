from employees.models import Employee


def default_employee_image(request):
    """Возвращает название фото пользователя по умолчанию"""

    if 'admin' in request.path:
        return {}
    else:
        return {
            'default_employee_image': Employee._meta.get_field('employee_photo').default
        }

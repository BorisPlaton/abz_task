from typing import Optional, Any

from django.http import Http404

from employees.forms import EmployeeEditForm
from employees.models import Employee
from employees.services.images import ProfilePhoto


def return_404_if_none(item: Any) -> Any:
    """Проверяет, что item есть и возвращает его, иначе вызывает 404 ошибку"""

    if not item:
        raise Http404

    return item


def get_employee_by_slug(slug: str) -> Optional[Employee]:
    """
    Возвращает работника по slug'у.

    Возвращает экземпляр класса Employee по slug'y, если такого нет,
    то возвращает None.
    """

    employee = (Employee.objects
                .select_related('position')
                .select_related('parent')
                .filter(slug=slug))

    if employee.exists():
        return employee.first()


def save_employee_from_form(form: EmployeeEditForm) -> Employee:
    """Сохраняет данные пользователя из формы"""
    
    employee = form.save()
    profile_pic = ProfilePhoto(employee.employee_photo.path)
    profile_pic.get_square_photo()
    profile_pic.save()

    return employee



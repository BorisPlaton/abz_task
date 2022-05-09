from typing import Optional, Any

from django.db.models import QuerySet, Q
from django.http import Http404

from employees.forms import EmployeeEditForm
from employees.models import Employee


def return_404_if_none(item: Any) -> Any:
    """Проверяет, что `item` есть и возвращает его, иначе вызывает 404 ошибку"""

    if not item:
        raise Http404

    return item


def get_employee_by(params: dict) -> Optional[Employee]:
    """
    Возвращает работника по параметрам `params`.

    :param params: Словарь с полем и его значением, по которому
        осуществляется поиск.
    """

    employee = (Employee.objects
                .select_related('position')
                .select_related('parent')
                .filter(**params))

    if employee.exists():
        return employee.first()


def get_employees_by_keyword(keyword: str) -> Optional[QuerySet]:
    """
    Возвращает `QuerySet` из работников, у которых поле совпадает
    со значением `keyword`.

    :param keyword: Строка, по которой ищутся совпадения в полях записи.
    """

    if not keyword:
        return Employee.objects.select_related('position').select_related('parent').all()

    return (Employee.objects
            .select_related('position')
            .select_related('parent')
            .filter(Q(first_name__icontains=keyword) |
                    Q(second_name__icontains=keyword) |
                    Q(patronymic__icontains=keyword) |
                    Q(date_employment__icontains=keyword) |
                    Q(payment__icontains=keyword) |
                    Q(position__title__icontains=keyword)).all()
            )


def save_employee_from_form(form: EmployeeEditForm, commit: bool = True) -> Employee:
    """
    Сохраняет данные пользователя из формы.

    :param form: экземпляр `EmployeeEditForm` класса.
    :param commit: Передается в `save()` метод.
    """

    print(commit)
    employee = form.save(commit)

    return employee


def delete_employee_photo(employee) -> None:
    """
    Удаляет фото работника.

    Если это не стандартное фото, то удаляет его и ставит фото по умолчанию,
    иначе ничего не делает.

    :param employee: экземпляр `Employee` класса.
    """

    if employee.employee_photo != Employee._meta.get_field('employee_photo').default:
        employee.employee_photo = Employee._meta.get_field('employee_photo').default
        employee.save()


def collect_search_bar_info(request) -> dict[str]:
    """
    Возвращает значение параметров из строки url после поиска сотрудника.

    :param request: `GET` запрос.
    """

    fields_name = [
        'keyword',
        'first_name',
        'second_name',
        'patronymic',
        'position__title',
        'payment',
        'parent__second_name',
        'date_employment',
    ]

    options = {field_name: request.get(field_name, '') for field_name in fields_name}
    return options


def sort_by_field_options(models: QuerySet, fields: list[str]) -> QuerySet:
    """
    Сортирует `models` по полям `options` в порядке возрастания.

    Возвращает отсортированный QuerySet.

    :param models: `Queryset`.
    :param fields: поля, по которым нужно отсортировать `models`. Сортировка
        происходит в той последовательности, в которой лежат названия полей.
    """

    return models.order_by(*fields).all()


def delete_employee(employee_pk: int) -> bool:
    """
    Удаляет экземпляр модели `Employee`.

    Возвращает True, если модель была удалена, иначе False.

    :param employee_pk: поле `primary key` записи.
    """

    employee = Employee.objects.filter(pk=employee_pk)

    if employee.exists():

        workers = employee.first().get_children()
        parent = employee.first().parent
        if workers and parent:
            workers.update(parent=parent)

        employee.delete()
        return True

    return False

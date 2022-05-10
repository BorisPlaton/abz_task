from typing import Optional, Any, Union

from django.core.paginator import Paginator
from django.db.models import QuerySet, Q
from django.db.models.base import ModelBase
from django.http import Http404

from employees.forms import EmployeeEditForm
from employees.models import Employee, Position


def return_404_if_none(item: Any) -> Any:
    """Проверяет, что `item` есть и возвращает его, иначе вызывает 404 ошибку"""

    if not item:
        raise Http404

    return item


def get_by(model: ModelBase, params: dict, join_models: list = None) -> Optional[ModelBase]:
    """
    Возвращает экземпляр модели `model` по параметрам `params`.

    :param model: Модель, в которой происходит поиск записи.
    :param params: Словарь с полем и его значением, по которому
        осуществляется поиск.
    :param join_models: Модели, которые надо присоединить к записи.
    """

    record = model.objects.filter(**params)

    if not record.exists():
        return

    if not join_models:
        return record.first()

    for model in join_models:
        record = record.select_related(model)

    return record.first()


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


def get_model_paginator(
        model: Union[QuerySet, ModelBase],
        page_num: int,
        records_per_page: int,
        on_each_side: int = 2,
        on_ends: int = 1) -> tuple[Paginator, list]:
    """
    Возвращает объект `Paginator` модели `model`.

    :param model: Объект `QuerySet` или `ModelBase`, от которого получают `Paginator`.
    :param page_num: Номер страницы.
    :param records_per_page: Количество записей на одной странице.
    :param on_ends: Количество страниц по сторонам на строке навигации.
    :param on_each_side: Количество страниц по сторонам от текущей страницы на строке навигации.
    """

    if isinstance(model, ModelBase):
        model = model.objects.all()

    paginator = Paginator(model, records_per_page)
    page_obj = paginator.get_page(page_num)
    page_list = paginator.get_elided_page_range(page_num, on_each_side=on_each_side, on_ends=on_ends)

    return page_obj, page_list


def get_positions() -> QuerySet:
    """Возвращает все должности из базы данных"""

    return Position.objects.all()


def delete_record_by_pk(model: ModelBase, pk: int) -> bool:
    """
    Удаляет запись из модели `model` по параметру `pk`.

    :param model: Модель из которой удаляют запись.
    :param pk: `id`, `primary key` модели.
    """

    record = model.objects.filter(pk=pk)

    if not record.exists():
        return False

    record.delete()
    return True

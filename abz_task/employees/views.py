from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from employees.forms import EmployeeEditForm, EditPositionForm
from employees.models import Employee, Position
import employees.services.services as sv


def home(request):
    """Каталог сотрудников в древовидной форме"""

    employees = (Employee.objects
                 .select_related('position')
                 .all())

    return render(
        request,
        'employees/home.html',
        {'employees': employees}
    )


def employees_list(request):
    """Список всех сотрудников"""

    options = sv.collect_search_bar_info(request.GET)
    employees = sv.sort_by_field_options(
        sv.get_employees_by_keyword(options.get('keyword')),
        [option for option in options if (options[option] and option != 'keyword')]
    )

    return render(
        request,
        'employees/employees_list.html',
        {
            'employees': sv.get_model_paginator(employees, request.GET.get('page', 1), 100),
            'options': options,
        }
    )


def employee_details(request, employee_slug):
    """
    Данные работника.

    :param employee_slug: `Slug` конкретного работника.
    """

    employee = sv.return_404_if_none(sv.get_by(Employee, {'slug': employee_slug}, ['parent', 'position']))

    return render(
        request,
        'employees/employee_details.html',
        {'employee': employee}
    )


@login_required
def create_employee(request):
    """Создание работника"""

    form = EmployeeEditForm(
        request.POST or None,
        request.FILES or None,
    )

    if form.is_valid():
        employee = sv.save_employee_from_form(form)
        messages.success(request, 'Работник создан')
        return redirect(employee.get_absolute_url())

    return render(
        request,
        'employees/create_employee.html',
        {'form': form}
    )


@login_required
def edit_employee(request, employee_slug):
    """
    Изменение данных сотрудника.

    :param employee_slug: `slug` работника, по которому получается модель.
    """

    form = EmployeeEditForm(
        request.POST or None, request.FILES or None,
        instance=sv.return_404_if_none(sv.get_by(Employee, {'slug': employee_slug}, ['parent', 'position'])),
    )

    if form.is_valid():
        employee = sv.save_employee_from_form(form)
        messages.success(request, 'Данные обновлены')
        return redirect(employee.get_absolute_url())

    return render(
        request,
        'employees/edit_employee.html',
        {
            'form': form,
            'employee_slug': employee_slug,
        }
    )


@login_required
def delete_photo(request, employee_pk):
    """
    Удаляет фото работника.

    :param employee_pk: id экземпляра.
    """

    employee = sv.return_404_if_none(sv.get_by(Employee, {'pk': employee_pk}, ['parent', 'position']))
    sv.delete_employee_photo(employee)

    return redirect(employee.get_absolute_url())


@login_required
def delete_employee(request, employee_pk):
    """
    Удаление экземпляра модели `Employee`.

    :param employee_pk: id экземпляра.
    """

    sv.return_404_if_none(sv.delete_employee(employee_pk))
    messages.success(request, 'Работник был удалён')

    return redirect('employees:home')


def positions_list(request):
    """Показывает все существующие должности"""

    return render(
        request,
        'employees/positions_list.html',
        {
            'positions': sv.get_model_paginator(
                Position, request.GET.get('page', 1), 100
            )
        }
    )


@login_required
def position_details(request, position_pk):
    """
    Страница должности.

    :param position_pk: `id`, `primary key` записи модели `Position`.
    """

    position = sv.return_404_if_none(sv.get_by(Position, {'pk': position_pk}))
    form = EditPositionForm(request.POST or None, instance=position)

    if form.is_valid():
        position = form.save()
        return redirect(position.get_absolute_url())

    return render(
        request,
        'employees/position_details.html',
        {
            'position': position,
            'form': form,
        }
    )


@login_required
def delete_position(request, position_pk):
    """
    Удаление должности по ключу `position_pk`.

    :param position_pk: `id`, `primary key` записи модели `Position`.
    """

    sv.return_404_if_none(sv.delete_record_by_pk(Position, position_pk))

    messages.success(request, 'Должность была удалена')

    return redirect('employees:home')


@login_required
def create_position(request):
    """Создание должности"""

    form = EditPositionForm(request.POST or None)

    if form.is_valid():
        position = form.save()
        return redirect(position.get_absolute_url())

    return render(
        request,
        'employees/create_position.html',
        {'form': form}
    )

from django.shortcuts import render

from employees.forms import EmployeeEditForm
from employees.models import Employee
from employees.services import get_employee_by_slug, return_404_if_none


def home(request):
    """Каталог сотрудников в древовидной форме"""

    employees = (Employee.objects
                 .select_related('position')
                 .all())
    context = {
        'employees': employees,
    }

    return render(
        request,
        'employees/home.html',
        context=context,
    )


def employees_list(request):
    """Список всех сотрудников"""

    employees = (Employee.objects
                 .select_related('position')
                 .select_related('parent')
                 .all())
    context = {
        'employees': employees,
    }

    return render(request, 'employees/employees_list.html', context=context)


def employee_details(request, employee_slug):
    """Данных работника"""

    employee = return_404_if_none(get_employee_by_slug(employee_slug))
    context = {
        'employee': employee,
    }

    return render(request, 'employees/employee_details.html', context=context)


def edit_employee(request, employee_slug):
    """Изменение данных сотрудника"""

    form = EmployeeEditForm(request.POST or None, instance=return_404_if_none(get_employee_by_slug(employee_slug)))
    context = {
        'form': form,
        'employee_slug': employee_slug,
    }

    return render(request, 'employees/edit_employee.html', context=context)

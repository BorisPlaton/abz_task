from django.shortcuts import render

from employees.models import Employee
from employees.services import get_employee_by_slug


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


def employee_details(request, slug):
    """Страница данных работника"""

    employee = get_employee_by_slug(slug)
    context = {
        'employee': employee,
    }

    return render(request, 'employees/employee_details.html', context=context)

from django.contrib import messages
from django.shortcuts import render, redirect

from employees.forms import EmployeeEditForm
from employees.models import Employee
from employees.services.services import return_404_if_none, get_employee_by_slug, save_employee_from_form, \
    get_employee_by_pk, delete_employee_photo


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

    if request.POST:
        form = EmployeeEditForm(
            request.POST,
            request.FILES,
            instance=return_404_if_none(get_employee_by_slug(employee_slug))
        )
        if form.is_valid():
            employee = save_employee_from_form(form)
            messages.success(request, 'Данные обновлены')
            return redirect('employees:edit_employee', employee.slug)
    else:
        form = EmployeeEditForm(
            instance=return_404_if_none(get_employee_by_slug(employee_slug))
        )

    context = {
        'form': form,
        'employee_slug': employee_slug,
    }

    return render(request, 'employees/edit_employee.html', context=context)


def delete_photo(request, employee_pk):
    """Удаляет фото работника"""

    employee = return_404_if_none(get_employee_by_pk(employee_pk))
    delete_employee_photo(employee)

    return redirect(employee.get_absolute_url())

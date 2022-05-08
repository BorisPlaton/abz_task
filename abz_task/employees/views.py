from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from employees.forms import EmployeeEditForm
from employees.models import Employee
import employees.services.services as sv


def home(request):
    """Каталог сотрудников в древовидной форме"""

    employees = (Employee.objects
                 .select_related('position')
                 .all())

    return render(request, 'employees/home.html',
                  {
                      'employees': employees,
                  })


def employees_list(request):
    """Список всех сотрудников"""

    options = sv.collect_search_bar_info(request.GET)
    employees = sv.sort_by_field_options(
        sv.get_employees_by_keyword(options.get('keyword')),
        [option for option in options if (options[option] and option != 'keyword')]
    )
    paginator = Paginator(employees, 100).get_page(request.GET.get('page', 1))

    return render(request, 'employees/employees_list.html',
                  {
                      'employees': paginator,
                      'options': options,
                  })


def employee_details(request, employee_slug):
    """Данных работника"""

    employee = sv.return_404_if_none(sv.get_employee_by({'slug': employee_slug}))

    return render(request, 'employees/employee_details.html',
                  {
                      'employee': employee,
                  })


@login_required
def edit_employee(request, employee_slug):
    """Изменение данных сотрудника"""

    if request.POST:
        form = EmployeeEditForm(
            request.POST,
            request.FILES,
            instance=sv.return_404_if_none(sv.get_employee_by({'slug': employee_slug}))
        )
        if form.is_valid():
            employee = sv.save_employee_from_form(form)
            messages.success(request, 'Данные обновлены')
            return redirect('employees:edit_employee', employee.slug)
    else:
        form = EmployeeEditForm(
            instance=sv.return_404_if_none(sv.get_employee_by({'slug': employee_slug}))
        )

    return render(request, 'employees/edit_employee.html',
                  {
                      'form': form,
                      'employee_slug': employee_slug,
                  })


@login_required
def delete_photo(request, employee_pk):
    """Удаляет фото работника"""

    employee = sv.return_404_if_none(sv.get_employee_by({'pk': employee_pk}))
    sv.delete_employee_photo(employee)

    return redirect(employee.get_absolute_url())

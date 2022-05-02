from django.db.models import Count
from django.shortcuts import render

from employees.models import Employee


def home(request):
    """Каталог сотрудников"""

    employees = (
        Employee.objects
        .select_related('position')
        .filter(boss=None)
        .annotate(children_amount=Count('workers'))
        .all()
    )
    context = {
        'employees': employees,
    }

    return render(request, 'employees/home.html', context=context)

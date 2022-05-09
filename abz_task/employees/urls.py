from django.urls import path
from . import views


app_name = 'employees'

urlpatterns = [
    path('', views.home, name='home'),
    path('employees_list/', views.employees_list, name='employees_list'),
    path('employee/<slug:employee_slug>/', views.employee_details, name='employee_details'),
    path('edit_employee/<slug:employee_slug>/', views.edit_employee, name='edit_employee'),
    path('delete_photo/<int:employee_pk>', views.delete_photo, name='delete_photo'),
    path('delete_employee/<int:employee_pk>', views.delete_employee, name='delete_employee'),
]

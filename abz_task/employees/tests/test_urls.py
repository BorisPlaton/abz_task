import datetime

import pytz
from django.test import TestCase
from django.urls import reverse

from employees.models import Employee, Position


class URLStatusTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.position = Position.objects.create(title='Повар')
        cls.employee = Employee.objects.create(
            first_name='Дмитрий',
            second_name='Александров',
            patronymic='Николаевич',
            date_employment=datetime.datetime(2022, 9, 14, 12, 33, 41, tzinfo=pytz.UTC),
            payment=2000,
            position=cls.position,
            parent=None,
        )

    def test_anonymous_user_response_status_home_page(self):
        response = self.client.get(reverse('employees:home'))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_response_status_employees_list(self):
        response = self.client.get(reverse('employees:employees_list'))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_response_status_employee_page(self):
        response = self.client.get(reverse('employees:employee_details', args=[self.employee.slug]))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_response_status_create_employee(self):
        response = self.client.get(reverse('employees:create_employee'))
        self.assertEqual(response.status_code, 302)

    def test_anonymous_user_response_status_edit_employee(self):
        response = self.client.get(reverse('employees:edit_employee', args=[self.employee.slug]))
        self.assertEqual(response.status_code, 302)

    def test_anonymous_user_response_status_delete_photo(self):
        response = self.client.get(reverse('employees:delete_photo', args=[self.employee.pk]))
        self.assertEqual(response.status_code, 302)

    def test_anonymous_user_response_status_delete_employee(self):
        response = self.client.get(reverse('employees:delete_employee', args=[self.employee.pk]))
        self.assertEqual(response.status_code, 302)

    def test_anonymous_user_response_status_positions_list(self):
        response = self.client.get(reverse('employees:positions_list'))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_response_status_position_details(self):
        response = self.client.get(reverse('employees:position_details', args=[self.position.pk]))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_response_status_delete_position(self):
        response = self.client.get(reverse('employees:delete_position', args=[self.position.pk]))
        self.assertEqual(response.status_code, 302)

    def test_anonymous_user_response_status_create_position(self):
        response = self.client.get(reverse('employees:create_position'))
        self.assertEqual(response.status_code, 302)

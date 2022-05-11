import datetime

import pytz
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from employees.models import Employee, Position

User = get_user_model()


class EmployeesEmployeeViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.credentials = {
            'username': 'boris_platon',
            'password': 'qwerty'
        }
        cls.user = User.objects.create_user(**cls.credentials)

    def setUp(self):
        self.employee_data = {
            'first_name': 'Дмитрий',
            'second_name': 'Александров',
            'patronymic': 'Николаевич',
            'date_employment': datetime.datetime(2022, 9, 14, 12, 33, 41, tzinfo=pytz.UTC),
            'payment': 2000,
            'position': '',
            'parent': '',
            'employee_photo': '',
        }
        self.created_employee_data = {
            'first_name': 'Василий',
            'second_name': 'Васильев',
            'patronymic': 'Васильевич',
            'date_employment': datetime.datetime(2022, 9, 14, 12, 33, 41, tzinfo=pytz.UTC),
            'payment': 1200,
            'position': None,
            'parent': None,
        }
        self.created_employee = Employee.objects.create(**self.created_employee_data)
        self.client.login(**self.credentials)

    def test_create_employee_with_correct_data(self):
        self.assertEqual(self.employee_amount, 1)
        self.client.post(reverse('employees:create_employee'), self.employee_data)
        self.assertEqual(self.employee_amount, 2)

    def test_create_employee_with_incorrect_data(self):
        self.employee_data.update({'date_employment': 'sss', 'payment': 'numbers'})
        self.client.post(reverse('employees:create_employee'), self.employee_data)
        self.assertEqual(self.employee_amount, 1)

    def test_redirect_after_create_employee_with_correct_data(self):
        response = self.client.post(reverse('employees:create_employee'), self.employee_data)
        self.assertEqual(response.status_code, 302)

    def test_edit_employee_with_correct_data(self):
        self.employee_data.update({'payment': 320, 'first_name': 'Иван'})
        self.client.post(
            reverse('employees:edit_employee', args=[self.created_employee.slug]),
            self.employee_data,
            follow=True,
        )
        self.created_employee.refresh_from_db()
        self.assertEqual(self.created_employee.payment, 320)
        self.assertEqual(self.created_employee.first_name, 'Иван')

    def test_edit_employee_with_incorrect_data(self):
        self.employee_data.update({'payment': 'ssss'})
        self.client.post(
            reverse('employees:edit_employee', args=[self.created_employee.slug]),
            self.employee_data,
        )
        self.created_employee.refresh_from_db()
        self.assertEqual(self.created_employee.payment, self.created_employee_data['payment'])

    def test_redirect_after_edit_employee_with_correct_data(self):
        self.employee_data.update({'payment': 320, 'first_name': 'Иван'})
        response = self.client.post(
            reverse('employees:edit_employee', args=[self.created_employee.slug]),
            self.employee_data
        )
        self.created_employee.refresh_from_db()
        self.assertEqual(response.status_code, 302)

    def test_delete_employee(self):
        self.assertEqual(self.employee_amount, 1)
        self.client.get(reverse('employees:delete_employee', args=[self.created_employee.pk]))
        self.assertEqual(self.employee_amount, 0)

    def test_delete_non_existent_employee(self):
        self.assertEqual(self.employee_amount, 1)
        response = self.client.get(reverse('employees:delete_employee', args=[32]), follow=True)
        self.assertEqual(self.employee_amount, 1)
        self.assertEqual(response.status_code, 404)

    @property
    def employee_amount(self):
        return Employee.objects.all().count()


class EmployeesPositionViewsTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.credentials = {
            'username': 'boris_platon',
            'password': 'qwerty'
        }
        cls.user = User.objects.create_user(**cls.credentials)

    def setUp(self) -> None:
        self.not_created_position_data = {
            'title': 'Barman'
        }
        self.created_position_data = {
            'title': 'Waitress'
        }
        self.created_position = Position.objects.create(**self.created_position_data)
        self.client.login(**self.credentials)

    def test_create_position_with_correct_data(self):
        self.assertEqual(self.position_amount, 1)
        self.client.post(reverse('employees:create_position'), self.not_created_position_data)
        self.assertEqual(self.position_amount, 2)

    def test_create_position_without_data(self):
        self.assertEqual(self.position_amount, 1)
        self.client.post(reverse('employees:create_position'), {'title': ''})
        self.assertEqual(self.position_amount, 1)

    def test_edit_position_with_correct_data(self):
        self.assertEqual(self.position_amount, 1)
        self.client.post(
            reverse('employees:position_details', args=[self.created_position.pk]),
            self.not_created_position_data
        )
        self.created_position.refresh_from_db()
        self.assertEqual(self.position_amount, 1)
        self.assertEqual(self.created_position.title, self.not_created_position_data['title'])

    def test_edit_position_without_data(self):
        self.assertEqual(self.position_amount, 1)
        self.client.post(reverse('employees:create_position'), {'title': ''})
        self.created_position.refresh_from_db()
        self.assertEqual(self.position_amount, 1)
        self.assertEqual(self.created_position.title, self.created_position_data['title'])

    def test_delete_position(self):
        self.client.post(reverse('employees:delete_position', args=[self.created_position.pk]))
        self.assertFalse(self.position_amount)

    @property
    def position_amount(self):
        return Position.objects.all().count()

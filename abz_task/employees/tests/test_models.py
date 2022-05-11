import datetime

import pytz
from django.test import TestCase
from django.urls import reverse

from employees.models import Position, Employee


class PositionModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.position_instance = Position.objects.create(title='Повар')
        cls.employee_instance = Employee.objects.create(
            first_name='Дмитрий',
            second_name='Александров',
            patronymic='Николаевич',
            date_employment=datetime.datetime(2022, 9, 14, 12, 33, 41, tzinfo=pytz.UTC),
            payment=2000,
            position=cls.position_instance,
            parent=None,
        )

    def test_position_str_method(self):
        self.assertEqual(str(self.position_instance), self.position_instance.title)

    def test_position_get_absolute_url_method(self):
        self.assertEqual(
            reverse('employees:position_details', args=[self.position_instance.pk]),
            self.position_instance.get_absolute_url()
        )

    def test_count_related_field_employees(self):
        self.assertEqual(self.position_instance.employees.count(), 1)


class EmployeeModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.position_instance = Position.objects.create(title='Повар')
        cls.employee_parent = Employee.objects.create(
            first_name='Дмитрий',
            second_name='Дмитров',
            patronymic='Дмитриевич',
            date_employment=datetime.datetime(2022, 9, 14, 12, 33, 41, tzinfo=pytz.UTC),
            payment=2000,
            position=cls.position_instance,
            parent=None,
        )
        cls.first_descendants_employee = Employee.objects.create(
            first_name='Василий',
            second_name='Васильев',
            patronymic='Васильевич',
            date_employment=datetime.datetime(2022, 9, 14, 12, 33, 41, tzinfo=pytz.UTC),
            payment=200,
            position=cls.position_instance,
            parent=cls.employee_parent,
        )
        cls.second_descendants_employee = Employee.objects.create(
            first_name='Николай',
            second_name='Николаев',
            patronymic='Николаевич',
            date_employment=datetime.datetime(2022, 9, 14, 12, 33, 41, tzinfo=pytz.UTC),
            payment=300,
            position=cls.position_instance,
            parent=cls.employee_parent,
        )

    def test_employee_str_method(self):
        self.assertEqual(
            str(self.employee_parent),
            f"{self.employee_parent.second_name} {self.employee_parent.first_name} {self.employee_parent.patronymic}",
        )

    def test_full_name_property(self):
        self.assertEqual(
            self.employee_parent.full_name,
            f"{self.employee_parent.second_name} {self.employee_parent.first_name} {self.employee_parent.patronymic}",
        )

    def test_descendants_equality_of_common_parent(self):
        self.assertEqual(
            self.first_descendants_employee.parent,
            self.second_descendants_employee.parent,
        )

    def test_absence_of_parent_descendants_after_deleting_him(self):
        self.employee_parent.delete()
        self.second_descendants_employee.refresh_from_db()
        self.first_descendants_employee.refresh_from_db()
        self.assertIsNone(self.second_descendants_employee.parent)
        self.assertIsNone(self.first_descendants_employee.parent)

    def test_presence_of_new_parent_in_descendants_after_deleting_him(self):
        self.new_employee = Employee.objects.create(
            first_name='Алексей',
            second_name='Алексеев',
            patronymic='Алексеевич',
            date_employment=datetime.datetime(2022, 9, 14, 12, 33, 41, tzinfo=pytz.UTC),
            payment=300,
            position=self.position_instance,
            parent=None,
        )
        self.employee_parent.parent = self.new_employee
        self.employee_parent.save()

        self.employee_parent.delete()
        self.second_descendants_employee.refresh_from_db()
        self.first_descendants_employee.refresh_from_db()

        self.assertEqual(self.first_descendants_employee.parent, self.new_employee)
        self.assertEqual(self.second_descendants_employee.parent, self.new_employee)

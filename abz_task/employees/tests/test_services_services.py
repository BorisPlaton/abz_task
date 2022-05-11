from django.http import Http404
from django.test import TestCase

from employees.models import Position
from employees.services.services import return_404_if_none, get_positions, delete_record_by_pk


class EmployeesServicesTests(TestCase):

    def test_error_result_at_return_404_if_none_func(self):
        self.assertRaises(Http404, return_404_if_none, None)

    def test_true_result_at_return_404_if_none_func(self):
        self.assertTrue(return_404_if_none('Something'))

    def test_empty_query_set_at_get_positions_func(self):
        self.assertFalse(get_positions().exists())

    def test_amount_records_at_get_positions_func(self):
        Position.objects.create(title='Position')
        self.assertEqual(get_positions().count(), 1)

    def test_delete_record_by_pk_without_records_in_model(self):
        self.assertFalse(delete_record_by_pk(Position, 1))

    def test_delete_record_by_pk_with_record_in_model(self):
        position_instance = Position.objects.create(title='Position')
        self.assertTrue(delete_record_by_pk(Position, position_instance.pk))
        self.assertFalse(Position.objects.all().count())

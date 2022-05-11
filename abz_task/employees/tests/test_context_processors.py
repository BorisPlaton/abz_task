from django.test import TestCase
from django.urls import reverse

from employees.models import Employee


class ContextProcessorsTests(TestCase):

    def test_context_default_employee_image_regular_url(self):
        response = self.client.get(reverse('employees:home'))
        self.assertEqual(
            response.context['default_employee_image'],
            Employee._meta.get_field('employee_photo').default
        )

    def test_context_default_employee_image_admin_url(self):
        response = self.client.get(reverse('admin:login'))
        self.assertIsNone(response.context.get('default_employee_image'))

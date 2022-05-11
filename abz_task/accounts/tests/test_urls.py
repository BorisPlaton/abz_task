from django.test import TestCase
from django.urls import reverse


class URLStatusTests(TestCase):

    def test_anonymous_user_response_status_register_page(self):
        response = self.client.get(reverse('employees:home'))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_response_status_login_page(self):
        response = self.client.get(reverse('employees:employees_list'))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_response_status_logout_link(self):
        response = self.client.get(reverse('employees:create_employee'))
        self.assertEqual(response.status_code, 302)

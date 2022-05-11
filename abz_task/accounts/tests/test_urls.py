from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class URLAnonymousStatusTests(TestCase):

    def test_anonymous_user_response_status_register_page(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_response_status_login_page(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_response_status_logout_link(self):
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)


class URLAuthenticatedUserTests(TestCase):

    def setUp(self) -> None:
        self.credentials = {
            'username': 'boris_platon',
            'password': 'qwerty'
        }
        self.user = User.objects.create_user(**self.credentials)
        self.client.login(**self.credentials)

    def test_authenticated_user_response_status_register_page(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_response_status_login_page(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_response_status_logout_link(self):
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)

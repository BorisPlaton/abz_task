from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse

User = get_user_model()


class LoginPageTests(TestCase):

    def setUp(self) -> None:
        self.credentials = {
            'username': 'boris_platon',
            'password': 'qwerty'
        }
        self.user = User.objects.create_user(**self.credentials)

    def test_user_is_not_authenticated_before_login(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertFalse(response.context['user'].is_authenticated)

    def test_successful_login_process(self):
        response = self.client.post(reverse('accounts:login'), self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertEqual(response.context['user'].username, self.user.username)

    def test_redirect_after_login(self):
        response = self.client.post(reverse('accounts:login'), self.credentials)
        self.assertEqual(response.status_code, 302)

    def test_wrong_credentials_at_login_page(self):
        self.credentials.update({'password': 'qwerty1'})
        response = self.client.post(
            reverse('accounts:login'),
            self.credentials,
            follow=True
        )
        self.assertFalse(response.context['user'].is_authenticated)

    def test_logout_after_login(self):
        response = self.client.post(
            reverse('accounts:login'),
            self.credentials,
            follow=True
        )
        self.assertTrue(response.context['user'].is_authenticated)
        response = self.client.get(reverse('accounts:logout'), follow=True)
        self.assertFalse(response.context['user'].is_authenticated)


class RegisterPageTests(TestCase):

    def setUp(self) -> None:
        self.correct_credentials = {
            'username': 'boris_platon',
            'email': 'email@email.com',
            'password1': 'some_difficult_password1234',
            'password2': 'some_difficult_password1234'
        }
        self.wrong_credentials = {
            'username': 'wrong_user',
            'email': 'email@email.com',
            'password1': 'qwerty',
            'password2': 'wrong_password'
        }

    def test_successful_user_creation(self):
        self.assertEqual(self.users_amount, 0)
        self.client.post(reverse('accounts:register'), self.correct_credentials, follow=True)
        self.assertEqual(self.users_amount, 1)

    def test_user_is_authenticated_after_registration(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertFalse(response.context['user'].is_authenticated)
        response = self.client.post(reverse('accounts:register'), self.correct_credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_registration_with_wrong_credentials(self):
        response = self.client.post(reverse('accounts:register'), self.wrong_credentials, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertEqual(self.users_amount, 0)

    @property
    def users_amount(self):
        return User.objects.all().count()

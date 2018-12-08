import unittest

from django.test import Client
from django.test import TestCase
from django.urls import reverse

from .forms import *   # import all forms
from django.contrib.auth.models import User


class SignUpFormTest(TestCase):

    def test_SignUpForm_valid(self):
        form = SignUpForm(data={
            'email': "user@mp.com",
            'username': "user@mp.com",
            'password1': "longpassword",
            'password2': "longpassword",
            'first_name': "user",
            'last_name': "user"
        })

        self.assertTrue(form.is_valid())

    def test_invalid_mail(self):
        form = SignUpForm(data={
            'email': "user",
            'username': "user@mp.com",
            'password1': "longpassword",
            'password2': "longpassword",
            'first_name': "user",
            'last_name': "user"
        })
        self.assertFalse(form.is_valid())

    def test_passwords_not_matching(self):
        form = SignUpForm(data={
            'email': "user",
            'username': "user@mp.com",
            'password1': "longpassword1",
            'password2': "longpassword2",
            'first_name': "user",
            'last_name': "user"
        })
        self.assertFalse(form.is_valid())

    def test_required_fields(self):
        form = SignUpForm(data={
            'email': "user",
            'username': "user@mp.com",
            'password1': "longpassword1",
            'password2': "longpassword2"
        })
        self.assertFalse(form.is_valid())

    def test_SignUpForm_invalid(self):
        form = SignUpForm(data={
            'email': "",
            'password': "mp",
            'first_name': "mp",
            'phone': ""
        })
        self.assertFalse(form.is_valid())


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            'john',
            'lennon@thebeatles.com',
            'johnpassword'
        )

    def url_testing(self, url, status_code=200):  # pragma: no cover
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)

    def testLogin(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('accounts.index'))
        self.assertEqual(response.status_code, 200)

    def testLoginName(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('accounts.index'))
        self.assertEqual(str(response.context['user']), 'john')

    def testLogOut(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('accounts.signout'))
        self.assertNotEqual(str(response.context['user']), 'john')


class AccountsUrlsTestClass(TestCase):
    client = Client()

    def url_testing(self, url, status_code=200):  # pragma: no cover
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)

    def test_homepage_url(self):
        self.url_testing(reverse("accounts.index"))

    def test_signup_url(self):
        self.url_testing(reverse("accounts.signup"))

    def test_signout_url(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        self.client.login(username='testuser', password='12345')
        self.url_testing(reverse("accounts.signout"))

    def test_home_url(self):
        self.url_testing(reverse("accounts.home"), 302)

    def test_change_email(self):
        self.url_testing(reverse("change_email"), 302)

    def test_change_password(self):
        self.url_testing(reverse("change_password"), 302)

    def test_login(self):
        self.url_testing(reverse("accounts.login"))

    def test_signup(self):
        self.url_testing(reverse("accounts.signup"))

    def test_account_details_create(self):
        self.url_testing(reverse("accounts.details"), 302)

    def test_account_details_edit(self):
        self.url_testing(reverse("accounts.account"), 302)

    def test_account_details_update(self):
        self.url_testing(reverse("accounts.edit_account_details"), 302)

    def test_all_users_url(self):
        self.url_testing(reverse("accounts.list_users"), 302)

    def test_friends_url(self):
        self.url_testing(reverse('accounts.my_friends'), 302)

    def test_search_friends_url(self):
        self.url_testing(reverse("accounts.search_users"), 302)

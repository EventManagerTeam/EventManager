from django.test import TestCase
import unittest
from django.urls import reverse
from django.test import Client

from .forms import *   # import all forms


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


class AccountsUrlsTestClass(unittest.TestCase):
    client = Client()

    def url_testing(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_homepage_url(self):
        self.url_testing(reverse("accounts.index"))

    def test_signup_url(self):
        self.url_testing(reverse("accounts.signup"))

    def test_signout_url(self):
        self.url_testing(reverse("accounts.signout"))

    def test_home_url(self):
        self.url_testing(reverse("accounts.home"))

    def test_home_url(self):
        self.url_testing(reverse("accounts.login"))

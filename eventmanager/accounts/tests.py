from django.test import TestCase
import unittest
from django.urls import reverse
from django.test import Client


class AccountsTestClass(unittest.TestCase):
    client = Client()

    def test_homepage(self):
        url = reverse("accounts.index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

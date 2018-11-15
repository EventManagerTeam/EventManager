import unittest

from django.test import Client
from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User



class CategoriesTestCase(unittest.TestCase):
    def test_list_categories(self):
        pass

    def test_list_events_from_one_category(self):
        pass

class CategoriessUrlsTestClass(unittest.TestCase):
    client = Client()

    def url_testing(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_categories_url(self):
        self.url_testing(reverse("accounts.login"))

    def test_list_events_from_one_category_url(self):
        self.url_testing(reverse("accounts.login"))



import unittest

from categories.models import Category

from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from django.urls import reverse


class CategoriesTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            'john',
            'lennon@thebeatles.com',
            'johnpassword'
        )
        self.client.login(username='john', password='johnpassword')
        category = Category.objects.create(
            name='test event',
            description='cool description',
            slug="test",
        )

        self.category2 = Category.objects.create(
            name='fsdklfdklmfdskmfdkmlfksdmlfdms',
            description='different',
            slug='opa'
        )

    def test_list_categories(self):
        response = self.client.get(reverse('categories.listing'))
        self.assertEqual(response.status_code, 200)

    def test_list_categories_shows_news(self):
        response = self.client.get(reverse('categories.listing'))
        self.assertContains(response, 'test event')
        self.assertContains(response, 'fsdklfdklmfdskmfdkmlfksdmlfdms')

    def test_list_events_from_one_category(self):
        url = reverse('categories.all_from_category', kwargs={'slug': "test"})
        response = self.client.get(url)
        self.assertContains(response, 'test event')


class CategoriessUrlsTestClass(TestCase):
    client = Client()

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            'john',
            'lennon@thebeatles.com',
            'johnpassword'
        )
        self.client.login(username='john', password='johnpassword')
        category = Category.objects.create(
            name='test event',
            description='cool description',
            slug="test",
        )

    def url_testing(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_categories_url(self):
        self.url_testing(reverse("categories.listing"))

    def test_list_events_from_one_category_url(self):
        url = reverse("categories.all_from_category", kwargs={'slug': "test"})
        self.url_testing(url)

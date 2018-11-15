import unittest

from django.test import Client
from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User



class EventsTestCase(unittest.TestCase):
    def test_list_events(self):
        pass

    def test_create_event(self):
        pass

    def test_update_event(self):
        pass

    def test_delete_event(self):
        pass

    def test_view_event(self):
        pass


class EventsUrlsTestClass(unittest.TestCase):
    client = Client()

    def url_returns_200(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def url_redirects(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_list_events_url(self):
        self.url_returns_200(reverse("events.list"))

    def test_create_event_url(self):
        pass
        self.url_redirects(reverse("events.create_event"))

    def test_update_event_url(self):
        pass

    def test_delete_event_url(self):
        pass

    def test_view_event_url(self):
        pass


    # path('<slug:slug>', views.show_events_by_slug, name='events.event'),
    # path('<slug:slug>/delete', views.delete_event_by_slug, name='events.del'),


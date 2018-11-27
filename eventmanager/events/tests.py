import unittest

from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from categories.models import Category
from events.models import Event


class EventsTestCase(TestCase):
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

    def test_join_event(self):
        pass

    def test_unjoin_event(self):
        pass


class EventsFeedsTestCase(TestCase):
    def setUp(self):
        self.total_number_of_events = 25
        self.client = Client()

        self.client.login(username='john', password='johnpassword')
        category = Category.objects.create(
            name='test event',
            description='cool description',
            slug="test",
        )

        for event_id in range(self.total_number_of_events):
            eventstring = "test" + str(event_id)
            self.event = Event.objects.create(
                title=eventstring,
                description=eventstring,
            )
            self.event.save()
            self.event.category.add(category)
            self.event.save()

    def test_all_events_feed(self):
        response = self.client.get(reverse("event_feed"))
        latest_event = "test" + str(self.total_number_of_events - 1)
        self.assertContains(response, latest_event)
        self.assertContains(response, "test" + str(1))

    def test_latest_events_feed(self):
        response = self.client.get(reverse("latest_event_feed"))
        first_event_title = "test" + str(self.total_number_of_events)
        self.assertNotContains(response, first_event_title)
        latest_event_title = "test" + str(1)
        self.assertContains(response, latest_event_title)


class EventsUrlsTestClass(TestCase):
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

        self.event = Event.objects.create(
            title="testy",
            description='cool description',
            slug="event",
        )
        self.event.save()
        self.event.category.add(category)
        self.event.save()

    def url_returns_200(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_events_url(self):
        self.url_returns_200(reverse("events.list"))

    def test_create_event_url(self):
        self.url_returns_200(reverse("events.create_event"))

    def test_update_event_url(self):
        self.url_returns_200(reverse("events.edit", kwargs={'slug': "event"}))

    def test_delete_event_url(self):
        category = Category.objects.create(
            name='unisdjsd',
            description='cool description',
            slug="tesddssst",
        )
        self.event = Event.objects.create(
            title="delete",
            description='cool description',
            slug="delete",
            added_by=self.user,
        )
        self.event.save()
        self.event.category.add(category)
        self.url_returns_200(reverse("events.del", kwargs={'slug': "delete"}))

    def test_view_event_url(self):
        self.url_returns_200(reverse("event", kwargs={'slug': "event"}))

    def test_all_events_feed_url(self):
        self.url_returns_200(reverse("event_feed"))

    def test_latest_events_feed_url(self):
        self.url_returns_200(reverse("latest_event_feed"))

    def test_join_event(self):
        self.url_returns_200(reverse("events.join", kwargs={'slug': "event"}))

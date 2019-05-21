import unittest

from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from categories.models import Category
from events.models import Event


class ExportingLoggedTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            'john',
            'lennon@thebeatles.com',
            'johnpassword'
        )

        category = Category.objects.create(
            name='test event category',
            description='cool description',
            slug="test",
        )

        eventstring = "test"
        self.event = Event.objects.create(
            title=eventstring,
            description=eventstring,
            added_by=self.user,
            slug="randomslughere"
        )
        self.event.save()
        self.event.category.add(category)
        self.event.save()

        self.event2 = Event.objects.create(
            title=eventstring,
            description=eventstring,
            added_by=self.user,
            slug="randomslughere2"
        )
        self.event2.save()
        self.event2.category.add(category)
        self.event2.save()
        self.event2.team_members.add(self.user)
        self.client.login(username='john', password='johnpassword')

    def test_get_statistics_unavailable(self):
        response = self.client.get(
            reverse(
                'events.statistics', kwargs={'slug': "randomslughere"}
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Error")

    def test_get_statistics_available(self):
        response = self.client.get(
            reverse(
                'events.statistics', kwargs={'slug': "randomslughere2"}
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Comments")
        self.assertContains(response, "Views")
        self.assertContains(response, "Invites")

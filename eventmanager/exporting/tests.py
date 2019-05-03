import unittest

from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from categories.models import Category
from events.models import Event


class ExportingNotLoggedTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_export_as_json_not_logged_in(self):
        response = self.client.get(reverse('exporting/export_csv'))
        self.assertEqual(response.status_code, 302)

    def test_export_as_csv_not_logged_in(self):
        response = self.client.get(reverse('exporting/export_json'))
        self.assertEqual(response.status_code, 302)

    def test_export_logged_in(self):
        user = User.objects.create_user(
            'john',
            'lennon@thebeatles.com',
            'johnpassword'
        )
        self.client.login(username='john', password='johnpassword')

        response = self.client.get(reverse('exporting/export'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Error')


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

        for event_id in range(5):
            eventstring = "test" + str(event_id)
            self.event = Event.objects.create(
                title=eventstring,
                description=eventstring,
                added_by=self.user,
            )
            self.event.save()
            self.event.category.add(category)
            self.event.save()

        self.client.login(username='john', password='johnpassword')

    def test_export_as_json_logged_in_added_event(self):
        json_res = """
        [
            {
                "id": 1 ,
                "title": "test0" ,
                "description": "test0" ,
                "location": "" ,
                "country": "" ,
                "starts_at": "" ,
                "ends_at": ""
            } ,
            {
                "id": 2 ,
                "title": "test1" ,
                "description": "test1" ,
                "location": "" ,
                "country": "" ,
                "starts_at": "" ,
                "ends_at": ""
            } ,
            {
                "id": 3 ,
                "title": "test2" ,
                "description": "test2" ,
                "location": "" ,
                "country": "" ,
                "starts_at": "" ,
                "ends_at": ""
            } ,
            {
                "id": 4 ,
                "title": "test3" ,
                "description": "test3" ,
                "location": "" ,
                "country": "" ,
                "starts_at": "" ,
                "ends_at": ""
            } ,
            {
                "id": 5 ,
                "title": "test4" ,
                "description": "test4" ,
                "location": "" ,
                "country": "" ,
                "starts_at": "" ,
                "ends_at": ""
            }
        ]"""

        response = self.client.get(
            reverse(
                'exporting/export_json'
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, json_res)
        self.assertContains(response, 'test4')
        self.assertContains(response, 'test0')

    def test_export_as_csv_logged_in_added_event(self):
        response = self.client.get(reverse('exporting/export_json'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test4')
        self.assertContains(response, 'test0')

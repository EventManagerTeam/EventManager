import unittest

from django.test import Client
from django.test import TestCase
from django.urls import reverse

from accounts.models import AccountDetails

from categories.models import Category

from django.contrib.auth.models import User

from events.models import Event

from tasks.models import Task


class EventsTestCase(TestCase):
    def setUp(self):
        self.total_number_of_events = 5
        self.client = Client()
        self.user = User.objects.create_user(
            'john',
            'lennon@thebeatles.com',
            'johnpassword'
        )

        self.user.details = AccountDetails.objects.create(
            user=self.user,
            description='cool description',
            slug="userslug"
        )

        self.client.login(username='john', password='johnpassword')
        category = Category.objects.create(
            name='test event category',
            description='cool description',
            slug="test",
        )

        for event_id in range(self.total_number_of_events):
            eventstring = "test" + str(event_id)
            self.event = Event.objects.create(
                title=eventstring,
                description=eventstring
            )
            self.event.save()
            self.event.category.add(category)
            self.event.team_members.add(self.user)

            self.event.save()

        # create task
        self.task = Task.objects.create(title="Opaaaa", event=self.event,slug="slug")
        self.task.save()


    def test_delete_task_url_error(self):
    	user = User.objects.create_user(
    	    'test',
    	    'lennon@thebeatles.com',
    	    'johnpassword'
    	)
    	self.client.login(username='test', password='johnpassword')
    	url = reverse("tasks.delete_task", kwargs={'slug': self.event.slug, "task":"slug"})
    	response = self.client.get(url)
    	self.assertEqual(response.status_code, 200)


    def test_delete_task_url_returns_error(self):
    	user = User.objects.create_user(
    	    'test',
    	    'lennon@thebeatles.com',
    	    'johnpassword'
    	)
    	self.client.login(username='test', password='johnpassword')
    	url = reverse("tasks.delete_task", kwargs={'slug': self.event.slug, "task":"slug"})
    	response = self.client.get(url)
    	self.assertContains(response, "Error")

    def test_delete_task_url_success(self):
    	self.client.login(username='john', password='johnpassword')
    	url = reverse("tasks.delete_task", kwargs={'slug': self.event.slug, "task":"slug"})
    	response = self.client.get(url)
    	self.assertEqual(response.status_code, 302)

    def test_edit_task_url_error(self):
    	user = User.objects.create_user(
    	    'test',
    	    'lennon@thebeatles.com',
    	    'johnpassword'
    	)
    	self.client.login(username='test', password='johnpassword')
    	url = reverse("tasks.edit_task", kwargs={'slug': self.event.slug, "task":"slug"})
    	response = self.client.get(url)
    	self.assertEqual(response.status_code, 200)


    def test_edit_task_url_returns_error(self):
    	user = User.objects.create_user(
    	    'test',
    	    'lennon@thebeatles.com',
    	    'johnpassword'
    	)
    	self.client.login(username='test', password='johnpassword')
    	url = reverse("tasks.edit_task", kwargs={'slug': self.event.slug, "task":"slug"})
    	response = self.client.get(url)
    	self.assertContains(response, "Error")

    def test_edit_task_url_success(self):
    	self.client.login(username='john', password='johnpassword')
    	url = reverse("tasks.edit_task", kwargs={'slug': self.event.slug, "task":"slug"})
    	response = self.client.get(url)
    	self.assertEqual(response.status_code, 200)


    def test_edit_task_url_success_message(self):
    	self.client.login(username='john', password='johnpassword')
    	url = reverse("tasks.edit_task", kwargs={'slug': self.event.slug, "task":"slug"})
    	response = self.client.get(url)
    	self.assertContains(response, "Edit task:")
    	self.assertContains(response, self.task.title)


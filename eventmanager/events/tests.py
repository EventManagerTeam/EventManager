import datetime
import unittest

from accounts.models import AccountDetails
from categories.models import Category

from django.contrib.auth.models import User

from django.test import Client
from django.test import TestCase

from django.urls import reverse

from events.models import Comment
from events.models import Event
from events.models import Invite

from tasks.models import Task


class EventsTestCase(TestCase):
    def setUp(self):
        self.total_number_of_events = 25
        self.client = Client()

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
                description=eventstring,
            )
            self.event.save()
            self.event.category.add(category)
            self.event.save()

    def test_list_events_lists_event(self):
        url = reverse('events.list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"test1", resp.content)

    def test_list_events_lists_categories(self):
        url = reverse('events.list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'test event category', resp.content)

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

    def test_add_teammate(self):
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

        self.user.details = AccountDetails.objects.create(
            user=self.user,
            description='cool description',
            slug="userslug"
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
            added_by=self.user,
        )
        self.event.save()
        self.event.category.add(category)
        self.event.team_members.add(self.user)
        self.event.save()

    def url_returns_200(self, url, status_code=200):
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)

    def test_list_events_url(self):
        self.url_returns_200(reverse("events.list"))

    def test_create_event_url(self):
        self.url_returns_200(reverse("events.create_event"))

    def test_update_event_url(self):
        self.url_returns_200(reverse("events.edit", kwargs={'slug': "event"}))

    def test_delete_event_url(self):
        user = User.objects.create_user(
            'johnaaaa',
            'lennonaaa@thebeatles.com',
            'johnpasswordaaa'
        )

        self.client.login(username='johnaaaa', password='johnpasswordaaa')

        category = Category.objects.create(
            name='unisdjsd',
            description='cool description',
            slug="tesddssst",
        )
        event = Event.objects.create(
            title="delete",
            description='cool description',
            slug="delete",
            added_by=user,
        )
        event.save()
        event.category.add(category)
        self.url_returns_200(reverse("events.del", kwargs={'slug': "delete"}))

    def test_delete_event_url_unsuccessful(self):
        user = User.objects.create_user(
            'johnaaaa',
            'lennonaaa@thebeatles.com',
            'johnpasswordaaa'
        )

        user2 = User.objects.create_user(
            'johnaaaa2',
            'lennonaaa2@thebeatles.com',
            'johnpasswordaaa2'
        )
        self.client.login(username='johnaaaa', password='johnpasswordaaa')

        category = Category.objects.create(
            name='unisdjsd',
            description='cool description',
            slug="tesddssst",
        )
        event = Event.objects.create(
            title="delete",
            description='cool description',
            slug="delete",
            added_by=user2,
        )
        event.save()
        event.category.add(category)
        response = self.client.get(
            reverse(
                'events.del', kwargs={
                    'slug': "delete"}))
        self.assertEquals(response.status_code, 403)

    def test_view_event_url(self):
        user2 = User.objects.create_user(
            username='testuser2',
            password='12345'
        )

        user2.details = AccountDetails.objects.create(
            user=user2,
            description='cool description',
            slug="userslug2"
        )
        self.user.details.friends.add(user2)
        self.url_returns_200(reverse("event", kwargs={'slug': "event"}))

    def test_all_events_feed_url(self):
        self.url_returns_200(reverse("event_feed"))

    def test_latest_events_feed_url(self):
        self.url_returns_200(reverse("latest_event_feed"))

    def test_join_event(self):
        self.url_returns_200(reverse("events.join", kwargs={'slug': "event"}))

    def test_unjoin_event(self):
        self.url_returns_200(
            reverse(
                "events.rm_join",
                kwargs={
                    'slug': "event"}))

    def test_event_settings_url(self):
        self.url_returns_200(
            reverse(
                "events.settings",
                kwargs={
                    'slug': "event"}))

    def test_event_invites_url(self):
        self.url_returns_200(reverse("events.invites"))

    def test_event_invite_url(self):
        self.url_returns_200(
            reverse(
                "events.invite",
                kwargs={
                    'slug': 'userslug',
                    'event': "event"}))

    def test_event_url(self):
        self.url_returns_200(reverse("events.event", kwargs={'slug': "event"}))

    def test_add_team_member(self):
        user = User.objects.create_user(
            'johnaaaa',
            'lennonaaa@thebeatles.com',
            'johnpasswordaaa'
        )
        event = Event.objects.create(
            title="testy",
            description='cool description',
            slug="eventааааа",
            added_by=user,
        )
        self.client.login(username='johnaaaa', password='johnpasswordaaa')
        self.url_returns_200('events/userslug/eventааааа/add_teammate')

    def test_get_tasks_no_tasks(self):
        response = self.client.get(reverse('events.tasks'))
        self.assertContains(response, "TO DO:")
        self.assertContains(response, "DOING:")

        self.assertEqual(response.status_code, 200)

    def test_get_tasks(self):
        task_title = "Vey cooollll"
        self.task = Task.objects.create(
            title=task_title,
            event=self.event,
            slug="event",
            assignee=self.user,
            status="TODO"
        )
        response = self.client.get(reverse('events.tasks'))

        self.assertContains(response, task_title)
        self.assertEqual(response.status_code, 200)

    def test_confirm_invite(self):
        user2 = User.objects.create_user(
            'johnaaaa',
            'lennonaaa@thebeatles.com',
            'johnpasswordaaa'
        )
        Invite.objects.create(
            invited_user=self.user,
            invited_by=user2,
            event=self.event)
        self.url_returns_200(
            reverse(
                "events.confirm_invite",
                kwargs={
                    'slug': self.event.slug}))

    def test_decline_invite(self):
        user2 = User.objects.create_user(
            'johnaaaa',
            'lennonaaa@thebeatles.com',
            'johnpasswordaaa'
        )
        Invite.objects.create(
            invited_user=self.user,
            invited_by=user2,
            event=self.event)
        self.url_returns_200(
            reverse(
                "invites.decline_invite",
                kwargs={
                    'slug': self.event.slug}))

    def test_add_teammate(self):
        self.url_returns_200(
            reverse(
                "events.add_teammate",
                kwargs={
                    'slug': self.event.slug}))

        response = self.client.get(
            reverse(
                "events.add_teammate",
                kwargs={
                    'slug': self.event.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Find")

    def test_event_team_add(self):
        user2 = User.objects.create_user(
            'johnaaaa',
            'lennonaaa@thebeatles.com',
            'johnpasswordaaa'
        )

        response = self.client.get(
            reverse(
                "events.event_team_add",
                kwargs={
                    'slug': self.event.slug,
                    'user': user2
                }))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Success")
        self.assertContains(response, user2.username)

    def test_delete_comment_by_slug(self):
        Comment.objects.create(
            event=self.event,
            author=self.user,
            title="opaaa",
            content="sdasdsa")
        comment = Comment.objects.first()
        self.url_returns_200(
            reverse(
                "events.comment.del",
                kwargs={
                    'slug': self.event.slug,
                    'comment': comment.pk}))

    def test_edit_comment_by_slug(self):
        Comment.objects.create(
            event=self.event,
            author=self.user,
            title="opaaa",
            content="sdasdsa")
        comment = Comment.objects.first()

        response = self.client.get(
            reverse(
                "events.comment.edit",
                kwargs={
                    'slug': self.event.slug,
                    'comment': comment.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "opaaa")

    def test_event_board(self):
        self.url_returns_200(
            reverse(
                "events.board", kwargs={
                    'slug': self.event.slug}))

    def test_my_events(self):
        event = Event.objects.create(
            title="testy",
            description='cool description',
            slug="eventааааа",
            added_by=self.user,
        )
        event.attendees.add(self.user)
        response = self.client.get(reverse("events.my_events"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testy")

    def test_events_I_host(self):
        event = Event.objects.create(
            title="testy",
            description='cool description',
            slug="eventааааа",
            added_by=self.user,
        )
        event.attendees.add(self.user)
        response = self.client.get(reverse("events.events_I_host"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testy")

    def test_show_random_event(self):
        event = Event.objects.create(
            title="testy",
            description='cool description',
            slug="eventааааа",
            added_by=self.user,
        )
        response = self.client.get(reverse("events.show_random_event"))
        self.assertEqual(response.status_code, 302)

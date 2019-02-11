import unittest

from django.test import Client
from django.test import TestCase
from django.urls import reverse

from .forms import *
from django.contrib.auth.models import User

from accounts.models import AccountDetails
from accounts.models import FriendRequest


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


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            'john',
            'lennon@thebeatles.com',
            'johnpassword'
        )

    def url_testing(self, url, status_code=200):  # pragma: no cover
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)

    def test_login(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('accounts.index'))
        self.assertEqual(response.status_code, 200)

    def test_already_logged_in(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('accounts.login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign out")

    def test_login_name(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('accounts.index'))
        self.assertEqual(str(response.context['user']), 'john')

    def test_logout(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('accounts.signout'))
        self.assertNotEqual(str(response.context['user']), 'john')


class AccountsUrlsTestClass(TestCase):
    client = Client()

    def url_testing(self, url, status_code=200):  # pragma: no cover
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)

    def test_homepage_url(self):
        self.url_testing(reverse("accounts.index"))

    def test_signup_url(self):
        self.url_testing(reverse("accounts.signup"))

    def test_signup_url_when_logged_in(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        self.client.login(username='testuser', password='12345')
        self.url_testing(reverse("accounts.signup"))

    def test_signout_url(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        self.client.login(username='testuser', password='12345')
        self.url_testing(reverse("accounts.signout"))

    def test_home_url(self):
        self.url_testing(reverse("accounts.home"), 302)

    def test_home_url_logged(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        self.client.login(username='testuser', password='12345')
        self.url_testing(reverse("accounts.home"), 200)

    def test_change_email(self):
        self.url_testing(reverse("change_email"), 302)

    def test_change_password(self):
        self.url_testing(reverse("change_password"), 302)

    def test_login(self):
        self.url_testing(reverse("accounts.login"))

    def test_signup(self):
        self.url_testing(reverse("accounts.signup"))

    def test_account_details_create(self):
        self.url_testing(reverse("accounts.details"), 302)

    def test_account_details_edit(self):
        self.url_testing(reverse("accounts.account"), 302)

    def test_account_details_update(self):
        self.url_testing(reverse("accounts.edit_account_details"), 302)

    def test_all_users_url(self):
        self.url_testing(reverse("accounts.list_users"), 302)

    def test_friends_url(self):
        self.url_testing(reverse('accounts.my_friends'), 302)

    def test_search_friends_url(self):
        self.url_testing(reverse("accounts.search_users"), 302)

    def test_delete_account_logged(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        self.client.login(username='testuser', password='12345')

        self.url_testing(reverse("accounts.delete"), 200)

        response = self.client.get(reverse("accounts.delete"))
        self.assertContains(response, "Delete account")

    def test_delete_account_not_logged(self):
        self.url_testing(reverse("accounts.delete"), 302)

    def test_change_email_logged(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        self.client.login(username='testuser', password='12345')
        self.url_testing(reverse("change_email"))

    def test_change_password_logged(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        self.client.login(username='testuser', password='12345')
        self.url_testing(reverse("change_password"))

    def test_account_details_create_logged(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        self.client.login(username='testuser', password='12345')
        self.url_testing(reverse("accounts.details"))

    def test_account_details_edit_logged(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        self.user.details = AccountDetails.objects.create(
            user=self.user,
            description='cool description',
            slug="userslug"
        )
        self.client.login(username='testuser', password='12345')
        self.url_testing(reverse("accounts.account"))

    def test_account_details_update_logged(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        self.user.details = AccountDetails.objects.create(
            user=self.user,
            description='cool description',
            slug="userslug"
        )
        self.client.login(username='testuser', password='12345')
        self.url_testing(reverse("accounts.edit_account_details"))

    def test_all_users_url_logged(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        self.client.login(username='testuser', password='12345')
        self.url_testing(reverse("accounts.list_users"))

    def test_search_friends_url_logged(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        self.client.login(username='testuser', password='12345')
        self.url_testing(reverse("accounts.search_users"))

    def test_get_user_by_slug_url(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )

        user2 = User.objects.create_user(
            username='testuser2',
            password='12345'
        )

        self.user.details = AccountDetails.objects.create(
            user=self.user,
            description='cool description',
            slug="userslug"
        )

        user2.details = AccountDetails.objects.create(
            user=user2,
            description='cool description',
            slug="userslug2"
        )
        self.client.login(username='testuser', password='12345')
        self.user.details.friends.add(user2)
        self.url_testing(reverse('accounts.my_friends'))

    def test_get_user_by_slug_logic(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )

        user2 = User.objects.create_user(
            username='testuser2',
            password='12345'
        )

        user3 = User.objects.create_user(
            username='testuser3',
            password='12345'
        )

        self.user.details = AccountDetails.objects.create(
            user=self.user,
            description='cool description',
            slug="userslug"
        )

        user2.details = AccountDetails.objects.create(
            user=user2,
            description='cool description',
            slug="userslug2"
        )
        self.client.login(username='testuser', password='12345')
        self.user.details.friends.add(user2)
        response = self.client.get(reverse('accounts.my_friends'))
        self.assertContains(response, "testuser2")
        self.assertNotContains(response, "testuser3")

    def test_show_account_details_added(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )

        self.user.details = AccountDetails.objects.create(
            user=self.user,
            description='cool description',
            slug="userslug"
        )
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('accounts.account'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Profile picture ")

    def test_show_account_details_logged(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )

        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('accounts.account'))
        self.assertEqual(response.status_code, 200)

    def test_list_users(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )

        self.user.details = AccountDetails.objects.create(
            user=self.user,
            description='cool description',
            slug="userslug"
        )

        self.user2 = User.objects.create_user(
            username='testuser2',
            password='12345'
        )

        self.user.details = AccountDetails.objects.create(
            user=self.user2,
            description='cool description',
            slug="userslug2"
        )

        response = self.client.get(reverse('accounts.list_users'))
        self.assertEqual(response.status_code, 302)
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('accounts.list_users'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser2")

    def test_gеt_user_by_slug(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )

        self.user.details = AccountDetails.objects.create(
            user=self.user,
            description='cool description',
            slug="userslug"
        )

        response = self.client.get(
            reverse(
                'accounts.gеt_user_by_slug',
                kwargs={
                    'slug': "userslug"}))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "testuser")

        self.client.login(username='testuser', password='12345')
        response = self.client.get(
            reverse(
                'accounts.gеt_user_by_slug',
                kwargs={
                    'slug': "userslug"}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser")

    def test_show_account_details(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )

        self.user.details = AccountDetails.objects.create(
            user=self.user,
            description='cool description',
            slug="userslug"
        )
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('accounts.details'))


class FriendsTestClass(TestCase):
    def url_testing(self, url, status_code=200):  # pragma: no cover
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)

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

        self.user2 = User.objects.create_user(
            username='testuser',
            password='12345'
        )

        self.user2.details = AccountDetails.objects.create(
            user=self.user2,
            description='cool description',
            slug="userslug2"
        )
        self.client.login(username='john', password='johnpassword')

    def test_my_friend(self):
        self.user.details.friends.add(self.user2)
        self.user2.details.friends.add(self.user)

        self.url_testing(reverse("accounts.my_friends"))

    def test_unfriend(self):
        self.user.details.friends.add(self.user2)
        self.user2.details.friends.add(self.user)

        response = self.client.get(reverse('accounts.my_friends'))
        self.assertContains(response, "testuser")

        self.url_testing(
            reverse(
                "accounts.unfriend",
                kwargs={
                    'slug': "userslug2"}))

        response = self.client.get(reverse('accounts.my_friends'))
        self.assertNotContains(response, "testuser")

    def test_friend_logged(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(
            reverse(
                'accounts.add_friend', kwargs={
                    "slug": self.user2.details.slug}))
        self.assertContains(response, "Success!")

    def test_list_friendrequests_withoutrequests(self):
        response = self.client.get(reverse('accounts.list_friendrequests'))
        self.assertContains(response, "Friend requests")

    def test_list_friendrequests(self):
        FriendRequest.objects.create(sent_by=self.user2, sent_to=self.user)

        response = self.client.get(reverse('accounts.list_friendrequests'))

        self.assertContains(response, "Friend requests")

    def test_accept_request(self):
        FriendRequest.objects.create(sent_by=self.user2, sent_to=self.user)
        response = self.client.get(
            reverse(
                'accounts.accept_request',
                kwargs={
                    "slug": self.user2.details.slug}))
        self.assertContains(response, "successfully accepted friend request")
        self.assertEqual(response.status_code, 200)

    def test_decline_request(self):
        FriendRequest.objects.create(sent_by=self.user2, sent_to=self.user)
        response = self.client.get(
            reverse(
                'accounts.decline_request',
                kwargs={
                    "slug": self.user2.details.slug}))
        self.assertContains(response, "successfully declined friend request")
        self.assertEqual(response.status_code, 200)

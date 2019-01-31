from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from eventmanager.slugify import *

from mptt.querysets import TreeQuerySet


class AccountDetailsQuerySet(TreeQuerySet):
    def all(self):
        return self


class AccountDetailsManager(models.Manager):
    def get_queryset(self):
        return AccountDetailsQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()


class AccountDetails(models.Model):
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    slug = models.SlugField(unique=True, blank=True, null=True)

    profile_picture = models.ImageField(
        upload_to='profile_pictures',
        blank=True,
        null=True
    )

    friends = models.ManyToManyField(
        User,
        verbose_name=_("Friends"),
        blank=True,
        related_name="friends"
    )

    birth_date = models.DateField(("birthdate"), blank=True, null=True)

    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Plain text, any formatting or links will be removed"),
        unique=False,
        null=True,
        blank=True
    )

    def is_my_friend(user, friend):
        if AccountDetails.objects.filter(user=user).exists():
            my_details = AccountDetails.objects.get(user=user).friends.all()
            if AccountDetails.objects.filter(user=friend).exists():
                friend_details = AccountDetails.objects.get(
                    user=friend).friends.all()
                if user in friend_details:
                    return True
                if friend in my_details:
                    return True
        return False

    def get_my_friends(user):
        if AccountDetails.objects.filter(user=user).exists():
            friends = AccountDetails.objects.get(user=user).friends.all()

        for friend in friends:
            friend.details = AccountDetails.objects.get(user=friend)

        return friends

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        if not self.slug:
            unique_slugify(self, self.user.username)
        super().save_model(request, obj, form, change)

    class Meta(object):
        verbose_name = _("Account Details")
        verbose_name_plural = _("Account Details")

    def __str__(self):
        return "Details for: " + self.slug

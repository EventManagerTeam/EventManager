from accounts.models import AccountDetails

from categories.models import Category

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from django_countries.fields import CountryField

from mptt.querysets import TreeQuerySet

from datetime import date

from eventmanager.slugify import *

from tinymce.models import HTMLField


def future(value):
    today = date.today()
    if value < today:
        raise ValidationError("Can't add events that have ended")


class EventQuerySet(TreeQuerySet):
    def active(self):
        return self.filter(is_active=True)

    def sort(self):
        return self.order_by('title')


class EventManager(models.Manager):
    def get_queryset(self):
        return EventQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def sort(self):
        return self.get_queryset().sort()


class Event(models.Model):
    title = models.CharField(
        verbose_name=_("Title"),
        help_text=_("250 character limit"),
        max_length=250,
        unique=False,
        null=False,
        blank=False
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True
    )

    description = HTMLField(
        verbose_name=_("Description"),
        help_text=_("Plain text, any formatting or links will be removed"),
        unique=False,
        null=False,
        blank=False
    )

    location = models.CharField(
        verbose_name=_("Event Location"),
        help_text=_("400 character limit"),
        max_length=400,
        unique=False,
        null=True,
        blank=True
    )

    country = CountryField(
        blank=True,
        null=True
    )

    category = models.ManyToManyField(
        Category,
        verbose_name=_("Categories"),
        help_text=_("Can select many Categories"),
        blank=False,
        related_name="categories"
    )

    visibility = models.CharField(
        verbose_name=_("visibility"),
        unique=False,
        null=False,
        blank=False,
        default='1',
        max_length=2,
    )

    attendees = models.ManyToManyField(
        User,
        verbose_name=_("Attendees"),
        blank=True,
        related_name="attendees"
    )

    team_members = models.ManyToManyField(
        User,
        verbose_name=_("Team"),
        blank=True,
        related_name="team"
    )

    cover_image = models.ImageField(
        upload_to='events',
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        verbose_name=_("Is active"),
        default=True
    )

    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        auto_now_add=True
    )

    added_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    updated_at = models.DateTimeField(
        verbose_name=_("Updated at"),
        auto_now=True
    )
    starts_at = models.DateTimeField(
        verbose_name=_("Event starts at"),
        blank=True,
        null=True,
        validators=[future]
    )
    ends_at = models.DateTimeField(
        verbose_name=_("Event ends at"),
        blank=True,
        null=True,
        validators=[future]
    )

    objects = EventManager()

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)

    def has_joined_event(user, event_slug):
        try:
            attendees = Event.objects.get(slug=event_slug).attendees.all()
            return user in attendees
        except BaseException:
            return False

    def is_team_member(user, event_slug):
        try:
            team = Event.objects.get(slug=event_slug).team_members.all()
            return user in team
        except BaseException:
            return False

    def get_guests(event_slug):
        attendees = Event.objects.all().get(slug=event_slug).attendees.all()
        filtered_attendees = []
        for user in attendees:
            if AccountDetails.objects.filter(user=user):
                details = AccountDetails.objects.get(user=user)
                user.details = details
                filtered_attendees.append(user)
        return attendees

    def get_categories(event_slug):
        categories = Event.objects.all().get(slug=event_slug).category.all()
        filtered_category = []
        for name in categories:
            filtered_category.append(Category.objects.get(name=name))
        return filtered_category

    def get_category_names(event_slug):
        categories = Event.objects.all().get(slug=event_slug).category.all()
        filtered_category = ""
        for name in categories:
            filtered_category += Category.objects.get(name=name).name + ";"
        return filtered_category

    def can_view_event(event_slug, user):
        event_visibility = Event.objects.all().get(slug=event_slug).visibility
        event = Event.objects.all().get(slug=event_slug)
        has_joined_event = Event.has_joined_event(user, event)

        if has_joined_event:
            return True

        if event_visibility == '1':  # is for everyone
            return True

        if user.is_authenticated:
            if event_visibility == '2':  # is for logged in
                return True
            else:  # is for invited only
                return Invite.is_invited(user, event)
        return False

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.title)
        super(Event, self).save(*args, **kwargs)

    class Meta(object):
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        ordering = ['title']

    def __str__(self):
        return self.title


class CommentQuerySet(TreeQuerySet):
    def active(self):
        return self.filter(is_active=True)

    def sort(self):
        return self.order_by('name')


class CommentManager(models.Manager):
    def get_queryset(self):
        return CommentQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def sort(self):
        return self.get_queryset().sort()


class Comment(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        related_name='comments'
    )

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=120,
        unique=False,
        null=False,
        blank=False
    )

    content = HTMLField(
        verbose_name=_("Content"),
        unique=False,
        null=False,
        blank=False,
        max_length=500
    )

    is_active = models.BooleanField(
        verbose_name=_("Is active"),
        default=True
    )

    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        verbose_name=_("Updated at"),
        auto_now_add=True
    )

    objects = CommentManager()

    class Meta(object):
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ['created_at']

    def __str__(self):
        return self.title


class IniviteQuerySet(TreeQuerySet):
    def active(self):
        return self.filter(is_active=True)

    def sort(self):
        return self.order_by('name')


class IniviteManager(models.Manager):
    def get_queryset(self):
        return IniviteQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def sort(self):
        return self.get_queryset().sort()


class Invite(models.Model):

    invited_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='invited_user'
    )

    invited_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='invited_by'
    )

    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        related_name='event',
    )

    is_accepted = models.BooleanField(
        verbose_name=_("Is accepted"),
        default=False
    )

    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        auto_now_add=True
    )

    objects = IniviteManager()

    def is_invited(user, event):
        try:
            invite = Invite.objects.get(event=event, invited_user=user)
            return True
        except BaseException:
            return False

    class Meta(object):
        verbose_name = _("Invite")
        verbose_name_plural = _("Invites")

    def __str__(self):
        return self.invited_user.username

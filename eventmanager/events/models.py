from categories.models import Category
from django.db import models
from django.utils.translation import ugettext as _
from mptt.querysets import TreeQuerySet
from django.contrib.auth.models import User

from django.utils.text import slugify


class EventQuerySet(TreeQuerySet):
    def active(self):
        return self.filter(is_active=True)

    def sort(self):
        return self.order_by('name')


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

    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Plain text, any formatting or links will be removed"),
        unique=False,
        null=False,
        blank=False
    )

    category = models.ManyToManyField(
        Category,
        verbose_name=_("Categories"),
        help_text=_("Can select many Categories"),
        blank=False,
        related_name="categories"
    )

    visibility =  models.CharField(
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
        null=True
    )
    ends_at = models.DateTimeField(
        verbose_name=_("Event ends at"),
        blank=True,
        null=True
    )

    objects = EventManager()

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)

    def is_slug_used(slug):
        return Event.objects.filter(slug=slug).exists()

    def get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        unique_num = 1
        while Event.is_slug_used(unique_slug):
            unique_slug = '{}-{}'.format(slug, unique_num)
            unique_num += 1
        return unique_slug

    def has_joined_event(user, event_slug):
        attendees = Event.objects.all().get(slug=event_slug).attendees.all()
        return user in attendees

    def get_guests(event_slug):
        return Event.objects.all().get(slug=event_slug).attendees.all()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()
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

    content = models.TextField(
        verbose_name=_("Description"),
        unique=True,
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

    objects = IniviteManager()

    class Meta(object):
        verbose_name = _("Invite")
        verbose_name_plural = _("Invites")

    def __str__(self):
        return self.invited_user.username

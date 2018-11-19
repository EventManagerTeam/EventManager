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

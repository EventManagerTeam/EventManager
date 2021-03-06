from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from eventmanager.slugify import *

from mptt.querysets import TreeQuerySet


class CategoryQuerySet(TreeQuerySet):
    def active(self):
        return self.filter(is_active=True)

    def sort(self):
        return self.order_by('name')


class CategoryManager(models.Manager):
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def sort(self):
        return self.get_queryset().sort()


class Category(models.Model):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=254,
        unique=True,
        null=False,
        blank=False
    )

    slug = models.SlugField(unique=True, blank=True, null=True)

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
        auto_now=True
    )

    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Plain text, any formatting or links will be removed"),
        unique=False,
        null=True,
        blank=True
    )

    category_image = models.ImageField(
        upload_to='categories',
        blank=True,
        null=True
    )

    objects = CategoryManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.name)
        super(Category, self).save(*args, **kwargs)

    def number_of_events_in_category(self):
        from events.models import Event
        count = Event.objects.filter(category=self).count()
        return str(count) + " " + ('events' if count != 1 else 'event')

    class Meta(object):
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['name']

    def __str__(self):
        return self.name


class SuggestedCategory(models.Model):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=254,
        null=False,
        blank=False
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

    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Plain text, any formatting or links will be removed"),
        unique=False,
        null=True,
        blank=True
    )

    category_image = models.ImageField(
        upload_to='SuggestedCategories',
        blank=True,
        null=True
    )

    class Meta(object):
        verbose_name = _("Suggested Category")
        verbose_name_plural = _("Suggested Categories")
        ordering = ['name']

    def __str__(self):
        return self.name

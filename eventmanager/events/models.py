import os
from categories.models import Category
from django.db import models
from django.utils.translation import ugettext as _
class Event(models.Model):
    title = models.CharField(
        verbose_name=_("Title"),
        help_text=_("250 character limit"),
        max_length=250,
        unique=False,
        null=False,
        blank=False
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
        upload_to='eventmanager/media/events_covers/',
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
    class Meta(object):
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        ordering = ['title']
    def __str__(self):
        return self.title

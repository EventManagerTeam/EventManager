from django.db import models
from django.utils.translation import ugettext as _
from mptt.querysets import TreeQuerySet
from django.contrib.auth.models import User

from django.utils.text import slugify
from eventmanager.slugify import *
from events.models import Event


class TaskQuerySet(TreeQuerySet):
    def active(self):
        return self.filter(is_active=True)

    def sort(self):
        return self.order_by('name')


class TaskManager(models.Manager):
    def get_queryset(self):
        return TaskQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def sort(self):
        return self.get_queryset().sort()


STATUS_CHOICES = [
    ("TODO", "TODO"),
    ("DOING", "DOING"),
    ("DONE", "DONE"),
]


class Task(models.Model):
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

    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

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
        on_delete=models.CASCADE,
        related_name="added_by"
    )

    assignee = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="assigned_to"
    )

    updated_at = models.DateTimeField(
        verbose_name=_("Updated at"),
        auto_now=True
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    objects = TaskManager()

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        if not self.slug:
            unique_slugify(self, self.title)
        super().save_model(request, obj, form, change)

from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Event
from eventmanager import settings


class EventFeed(Feed):
    title = 'Events Feed'
    link = '/events/'
    description = 'Our latest events!'

    def items(self):
        return Event.objects.active().order_by('-created_at')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return "/events/" + item.slug


class LatestEventFeed(Feed):
    title = 'Events Feed'
    link = '/events/'
    description = 'Our latest events!'

    def items(self):
        return Event.objects.active().order_by('-created_at')[:settings.EVENTS_IN_FEED]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return "/events/" + item.slug
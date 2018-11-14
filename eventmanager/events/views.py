from django.shortcuts import render
from events.models import Event
from categories.models import Category

from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    events_list = Event.objects.active()
    number_of_items_per_page = 3
    paginator = Paginator(events_list, number_of_items_per_page)
    categories = Category.objects.active()
    page = request.GET.get('page', 1)

    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    return render(request, 'events/list_events.html', {'events': events,'categories':categories})


def show_events_by_slug(request, slug):
    event = Event.objects.active().get(slug=slug)
    return render(request, 'events/event.html', {'event': event})

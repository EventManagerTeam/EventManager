from django.shortcuts import render
from events.models import Event
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EventForm


def index(request):
    events_list = Event.objects.active()
    number_of_items_per_page = 5
    paginator = Paginator(events_list, number_of_items_per_page)

    page = request.GET.get('page', 1)

    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    return render(request, 'events/list_events.html', {'events': events})


def create_event(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
    return render(request, 'events/create_event.html', {'form': form})

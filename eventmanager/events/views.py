from django.shortcuts import render
from events.models import Event
from categories.models import Category
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EventForm


def index(request):
    events_list = Event.objects.active()
    number_of_items_per_page = 5
    paginator = Paginator(events_list, number_of_items_per_page)
    page = request.GET.get('page', 1)

    categories = Category.objects.active()
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    context = {'events': events, 'categories': categories}
    return render(request, 'events/list_events.html', context)


def create_event(request):

    if request.method == 'POST':

        form = EventForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.added_by = request.userг
            post.save()
    else:
        form = EventForm()

    return render(request, 'events/create_event.html', {'form': form})


def show_events_by_slug(request, slug):
    event = Event.objects.active().get(slug=slug)
    return render(request, 'events/event.html', {'event': event})

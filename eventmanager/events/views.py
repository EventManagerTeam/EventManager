from django.shortcuts import render
from events.models import Event
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    events_list = Event.objects.active()
    paginator = Paginator(events_list, 1)
    page = request.GET.get('page', 1)

    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    return render(request, 'events/list_events.html', {'events': events})

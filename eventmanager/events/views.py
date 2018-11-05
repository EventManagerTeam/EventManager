from django.shortcuts import render
from events.models import Event


def index(request):
    events = Event.objects.active()
    return render(request, 'events/list_events.html', {'events': events})

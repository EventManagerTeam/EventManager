from django.shortcuts import render

def index(request):
    return render(request, 'events/list_events.html')

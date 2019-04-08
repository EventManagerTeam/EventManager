from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from events.models import Event
from django.http import HttpResponse
from django.http import JsonResponse
from events.resources import EventResource


def get_user_events_dataset(user):
    queryset = Event.objects.filter(added_by=user)
    dataset = EventResource().export(queryset)
    return dataset


@login_required(login_url='/login')
def export_as_csv(request):
    dataset = get_user_events_dataset(request.user)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="persons.csv"'
    return response


@login_required(login_url='/login')
def export_as_json(request):
    dataset = get_user_events_dataset(request.user)
    response = HttpResponse(dataset.json, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="MyEvents.json"'
    return response


def export(request):
    if Event.objects.filter(added_by=request.user).count() > 0:
        return render(request, 'export/export.html')
    else:
        error_message = "Add events before trying to export them"
        context = {'error_message': error_message}
        return render(request, 'CRUDops/error.html', context)

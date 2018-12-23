from django.shortcuts import render
from tasks.models import Task
from events.models import Event
import events.views as event_views
from django.shortcuts import redirect
from django.urls import reverse


def delete_task(request, slug, task):
	event_id = Event.objects.get(slug=slug).pk
	Task.objects.filter(event=event_id).get(slug=task).delete()
	return redirect(reverse('events.board', kwargs={'slug': slug}))

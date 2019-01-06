import events.views as event_views

from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from events.forms import TaskForm
from events.models import Event

from tasks.models import Task


def delete_task(request, slug, task):
    members = Event.objects.get(slug=slug).team_members.all()
    if request.user in members:
        event_id = Event.objects.get(slug=slug).pk
        Task.objects.filter(event=event_id).get(slug=task).delete()
        return redirect(reverse('events.board', kwargs={'slug': slug}))
    else:
        error_message = "This event board is available only\
             to team members."
        context = {
            'error_message': error_message}
        return render(request, 'CRUDops/error.html', context)


def edit_task(request, slug, task):
    event_id = Event.objects.get(slug=slug).pk
    members = Event.objects.get(slug=slug).team_members.all()
    instance = Task.objects.get(slug=task)
    form = TaskForm(request.POST or None, instance=instance)

    if request.user in members:
        if request.method == 'POST':
            if form.is_valid():
                task = form.save(commit=False)
                task.added_by = request.user
                task.event_id = Event.objects.get(slug=slug).pk
                task.save()

            return redirect(reverse('events.board', kwargs={'slug': slug}))

    else:
        error_message = "This event board is available only\
             to team members."
        context = {
            'error_message': error_message}
        return render(request, 'CRUDops/error.html', context)

    context = {
        'task_form': form,
    }
    return render(request, 'tasks/edit_task.html', context)

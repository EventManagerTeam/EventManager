from .forms import CommentForm
from .forms import EventForm
from .forms import VisibilitySettings

from accounts.forms import UserForm
from accounts.models import AccountDetails
from categories.models import Category

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.core.exceptions import PermissionDenied
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator

from django.shortcuts import render

from eventmanager.slugify import *

from events.forms import TaskForm
from events.models import Comment
from events.models import Event
from events.models import Invite

from tasks.models import Task


def index(request):
    events_list = Event.objects.active()
    number_of_items_per_page = 5

    events = []
    for event in events_list:
        if Event.can_view_event(event.slug, request.user):
            events.append(event)

    events_list = events
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


def get_datetime(date, time):
    return date + " " + time


@login_required
def create_event(request):
    form = EventForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            event = form.save(commit=False)
            event.added_by = request.user

            if request.POST.get('starts_at') \
                    and request.POST.get('starts_at_time'):
                event.starts_at = get_datetime(
                    request.POST.get('starts_at'),
                    request.POST.get('starts_at_time')
                )

            if request.POST.get('ends_at') \
                    and request.POST.get('ends_at_time'):
                event.ends_at = get_datetime(
                    request.POST.get('ends_at'),
                    request.POST.get('ends_at_time')
                )
            if request.FILES.get('cover_image'):
                event.cover_image = request.FILES.get('cover_image')

            event.save()
            category = Category.objects.filter(
                name=request.POST["category_select"]
            )
            event.category.add(*list(category))
            event.attendees.add(request.user)
            event.team_members.add(request.user)
            event.save()
            context = {'success_message': "added new event"}
            return render(request, 'CRUDops/successfully.html', context)

    context = {'form': form, 'categories': Category.objects.active()}
    return render(
        request,
        'events/create_event.html',
        context
    )


def edit_event(request, slug):
    instance = Event.objects.all().get(slug=slug)
    form = EventForm(request.POST, request.FILES or None, instance=instance)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.added_by = request.user

            if request.POST.get('starts_at') \
                    and request.POST.get('starts_at_time'):
                post.starts_at = get_datetime(
                    request.POST.get('starts_at'),
                    request.POST.get('starts_at_time')
                )

            if request.POST.get('ends_at') \
                    and request.POST.get('ends_at_time'):
                post.ends_at = get_datetime(
                    request.POST.get('ends_at'),
                    request.POST.get('ends_at_time')
                )

            # if request.FILES['cover_image']:
            #     post.cover_image = request.FILES['cover_image']
            if request.FILES.get('cover_image'):
                event.cover_image = request.FILES.get('cover_image')
            post.save()

            category = Category.objects.filter(
                name=request.POST["category_select"]
            )
            post.category.add(*list(category))

            post.save()
            context = {
                'success_message': "edited event"
            }
            return render(request, 'CRUDops/successfully.html', context)

    starts_date = None
    starts_time = None

    if instance.starts_at:
        starts_date = str(instance.starts_at.date())
        starts_time = str(instance.starts_at.time())

    ends_date = None
    ends_time = None

    if instance.ends_at:
        ends_date = str(instance.ends_at.date())
        ends_time = str(instance.ends_at.time()),

    context = {
        'form': form,
        'categories': Category.objects.active(),
        'editing': True,
        'starts_date': starts_date,
        'ends_date': ends_date,
        'starts_time': starts_time,
        'ends_time': ends_time
    }
    return render(
        request,
        'events/create_event.html',
        context
    )


def show_events_by_slug(request, slug):
    event = Event.objects.active().get(slug=slug)
    if Event.can_view_event(slug, request.user) is True:
        comments = Comment.objects.active().sort()
        comments = comments.filter(event=event).order_by('-created_at')
        form = CommentForm(request.POST or None)
        username_form = UserForm(request.POST or None)

        storage = messages.get_messages(request)
        for message in storage:
            pass

        final_users = []
        final_team = []

        if request.user.is_authenticated:
            if AccountDetails.objects.filter(user=request.user).exists():
                users = AccountDetails.objects.get(
                    user=request.user).friends.all()
                for user in users:
                    if AccountDetails.objects.filter(user=user):
                        details = AccountDetails.objects.get(user=user)
                        user.details = details
                        final_users.append(user)

            if request.method == 'POST':
                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.event = event
                    comment.author = request.user
                    comment.save()

        has_joined = Event.has_joined_event(request.user, slug)

        team = event.team_members.all()
        for user in team:
            if AccountDetails.objects.filter(user=user):
                details = AccountDetails.objects.get(user=user)
                user.details = details
                final_team.append(user)

        context = {
            'event': event,
            'comments': comments,
            'form': form,
            'has_joined': has_joined,
            'guests': Event.get_guests(slug),
            'users': final_users,
            'team': final_team,
            'is_team_member': Event.is_team_member(request.user, slug)
        }
        return render(request, 'events/event.html', context)

    error_message = "Event is not available yet\
         or you don't have permission to view it."
    context = {
        'error_message': error_message}
    return render(request, 'CRUDops/error.html', context)


@login_required
def delete_event_by_slug(request, slug):
    event = Event.objects.get(slug=slug)
    if request.user == event.added_by:
        event.delete()
    else:
        raise PermissionDenied
    context = {'success_message': "deleted event"}
    return render(request, 'CRUDops/successfully.html', context)


@login_required
def join_event(request, slug):
    event = Event.objects.get(slug=slug)
    event.attendees.add(request.user)
    event.save()
    context = {'success_message': "joined event " + event.title}
    return render(request, 'CRUDops/successfully.html', context)


@login_required
def cancel_join(request, slug):
    event = Event.objects.get(slug=slug)
    event.attendees.remove(request.user)
    event.save()
    context = {'success_message': "removed going status from  " + event.title}
    return render(request, 'CRUDops/successfully.html', context)


@login_required
def invite(request, slug, event):
    logged_in_user = request.user
    logged_in_user_details = AccountDetails.objects.get(user=logged_in_user)
    other_user_details = AccountDetails.objects.get(slug=slug)
    invited_user = other_user_details.user

    event = Event.objects.get(slug=event)
    invite = Invite.objects.get_or_create(
        invited_user=invited_user,
        invited_by=logged_in_user,
        event=event)

    success_message = 'You have invited the user successfully'
    messages.success(request, success_message)
    return show_events_by_slug(request, event.slug)


@login_required
def invites(request):
    user = request.user
    invites = Invite.objects.filter(invited_user=user, is_accepted=False)

    context = {'events': invites}
    return render(request, 'events/invites.html', context)


@login_required
def tasks(request):
    user = request.user
    todo_tickets = Task.objects.filter(assignee=user).filter(status='TODO')
    doing_tickets = Task.objects.filter(assignee=user).filter(status='DOING')
    context = {'todo_tickets': todo_tickets, 'doing_tickets': doing_tickets}
    return render(request, 'events/my_tasks.html', context)


@login_required
def confirm_invite(request, slug):
    event = Event.objects.get(slug=slug)
    event.attendees.add(request.user)
    Invite.objects.filter(
        invited_user=request.user,
        event=event).update(
        is_accepted=True)
    return invites(request)


@login_required
def decline_invite(request, slug):
    event = Event.objects.get(slug=slug)
    Invite.objects.filter(
        invited_user=request.user,
        event=event).delete()
    return invites(request)


@login_required
def visibility_settings(request, slug):
    event = Event.objects.get(slug=slug)
    visibility_settings_form = VisibilitySettings(request.POST or None)

    if event.visibility != '1':
        visibility_settings_form = VisibilitySettings(
            request.POST or None, initial={
                'visibility': event.visibility})

    if request.method == 'POST':
        if visibility_settings_form.is_valid():
            visibility = visibility_settings_form.cleaned_data['visibility']
            Event.objects.filter(slug=slug).update(visibility=visibility)

    context = {
        'event': event,
        'visibility_settings_form': visibility_settings_form}
    return render(request, 'events/visibility_settings.html', context)


@login_required
def add_teammate(request, slug):
    event = Event.objects.get(slug=slug)
    form = UserForm(request.POST or None)

    context = {'form': form}
    filtered_users = []

    if request.method == 'POST':
        if form.is_valid():
            username = request.POST.get('username')
            users = User.objects.all().filter(username__icontains=username)
            for user in users:
                if AccountDetails.is_my_friend(request.user, user):
                    if AccountDetails.objects.filter(user=user):
                        details = AccountDetails.objects.get(user=user)
                        user.details = details
                    user.my_friend = AccountDetails.is_my_friend(
                        request.user, user)
                    filtered_users.append(user)
            context = {'users': filtered_users, 'form': form, 'event': event}

    return render(request, 'events/add_teammate.html', context)


@login_required
def event_team_add(request, user, slug):
    event = Event.objects.get(slug=slug)
    user = User.objects.get(username=user)
    members = Event.objects.get(slug=slug).team_members.all()
    if request.user not in members:
        event.team_members.add(request.user)
        if request.user not in Event.objects.get(slug=slug).attendees.all():
            event.attendees.add(request.user)

    if user not in members:
        event.team_members.add(user)
        if user not in Event.objects.get(slug=slug).attendees.all():
            event.attendees.add(user)

    context = {'success_message': "added new team member " +
               str(user) + " for event " + event.title}
    return render(request, 'CRUDops/successfully.html', context)


@login_required
def delete_comment_by_slug(request, slug, comment):
    Comment.objects.get(pk=comment).delete()
    return show_events_by_slug(request, slug)


@login_required
def edit_comment_by_slug(request, slug, comment):
    instance = Comment.objects.get(pk=comment)
    form = CommentForm(request.POST or None, instance=instance)

    if request.method == 'POST':
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'events/add_comment.html', context)


@login_required
def event_board(request, slug):
    members = Event.objects.get(slug=slug).team_members.all()

    event = Event.objects.get(slug=slug)
    todo_tickets = Task.objects.filter(status='TODO').filter(event_id=event.pk)
    doing_tickets = Task.objects.filter(
        status='DOING').filter(
        event_id=event.pk)
    done_tickets = Task.objects.filter(status='DONE').filter(event_id=event.pk)

    if request.user in members:
        form = TaskForm(request.POST or None)
        form.fields["assignee"].queryset = members
        if request.method == 'POST':
            if form.is_valid():
                task = form.save(commit=False)
                task.added_by = request.user
                unique_slugify(task, form.cleaned_data['title'])
                task.event_id = Event.objects.get(slug=slug).pk
                task.save()

        context = {
            'task_form': form,
            'todo_tickets': todo_tickets,
            'doing_tickets': doing_tickets,
            'done_tickets': done_tickets}
        return render(request, 'events/board.html', context)
    else:
        error_message = "This event board is available only\
             to team members."
        context = {
            'error_message': error_message}
        return render(request, 'CRUDops/error.html', context)


@login_required
def my_events(request):
    number_of_items_per_page = 5

    user = User.objects.get(username=request.user)
    events_list = Event.objects.filter(attendees=user)

    paginator = Paginator(events_list, number_of_items_per_page)
    page = request.GET.get('page', 1)
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    context = {'events': events}
    return render(request, 'events/list_my_events.html', context)

from django.shortcuts import render
from events.models import Event
from categories.models import Category
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EventForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import CommentForm
from events.models import Comment


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


def get_datetime(date, time):
    return date + " " + time


@login_required
def create_event(request):
    form = EventForm(request.POST or None)
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

            # post.cover_image = form.cleaned_data['image']
            post.save()
            category = Category.objects.filter(
                name=request.POST["category_select"]
            )
            post.category.add(*list(category))
            post.save()
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
    form = EventForm(request.POST or None, instance=instance)
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

            post.cover_image = request.POST.get('image')
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
    comments = Comment.objects.active()
    comments = comments.filter(event=event).order_by('-created_at')
    form = CommentForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.event = event
            comment.author = request.user
            comment.save()

    has_joined = False
    if Event.has_joined_event(request.user, slug):
        has_joined = True

    context = {
        'event': event,
        'comments': comments,
        'form': form,
        'has_joined': has_joined,
        'guests': Event.get_guests(slug)
    }
    return render(request, 'events/event.html', context)


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
    context = {'success_message': "joined event" + event.title}
    return render(request, 'CRUDops/successfully.html', context)


@login_required
def cancel_join(request, slug):
    event = Event.objects.get(slug=slug)
    event.attendees.remove(request.user)
    event.save()
    context = {'success_message': "not going event" + event.title}
    return render(request, 'CRUDops/successfully.html', context)

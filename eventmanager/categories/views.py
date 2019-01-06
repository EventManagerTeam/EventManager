from django.shortcuts import render

from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator

from categories.models import Category

from events.models import Event


def listing(request):
    categories = Category.objects.active().sort()
    chunks = [categories[x:x + 3] for x in range(0, len(categories), 3)]
    context = {'categories': chunks}
    return render(request, 'categories/all_categories.html', context)


def all_from_category(request, slug):
    category = Category.objects.get(slug=slug)
    events_list = Event.objects.filter(category=category)
    number_of_items_per_page = 3
    paginator = Paginator(events_list, number_of_items_per_page)

    page = request.GET.get('page', 1)

    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    categories = Category.objects.sort().active()
    context = {'events': events, 'categories': categories}
    return render(request, 'events/list_events.html', context)

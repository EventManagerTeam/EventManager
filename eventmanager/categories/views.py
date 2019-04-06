from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator

from categories.models import Category
from categories.models import SuggestedCategory

from events.models import Event
from categories.forms import SuggestedCategoryForm


def listing(request):
    categories = Category.objects.active().sort()
    chunks = [categories[x:x + 3] for x in range(0, len(categories), 3)]
    context = {'categories': chunks}
    return render(request, 'categories/all_categories.html', context)


def listing_suggested(request):
	if SuggestedCategory.objects.count() > 0:
	    categories = SuggestedCategory.objects.all()
	    chunks = [categories[x:x + 3] for x in range(0, len(categories), 3)]
	    context = {'categories': chunks}
	    return render(request, 'categories/all_categories.html', context)
	else:
		return render(request, 'categories/no_suggested.html')


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


@login_required(login_url='/login')
def suggest_category(request):
    form = SuggestedCategoryForm(request.POST or None, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            category = form.save(commit=False)
            category.added_by = request.user

            if request.FILES.get('category_picture'):
                category.category_image = request.FILES.get('category_picture')

            category.save()

            context = {'success_message': "suggested new category"}
            return render(request, 'CRUDops/successfully.html', context)

    context = {'form': form}
    return render(
        request,
        'categories/suggest_category.html',
        context
    )

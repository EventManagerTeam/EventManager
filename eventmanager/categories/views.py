from django.shortcuts import render
from categories.models import Category

def listing(request):
    categories = Category.objects.active()
    chunks = [categories[x:x + 3] for x in range(0, len(categories), 3)]
    return render(request, 'categories/all_categories.html', {'categories': chunks})
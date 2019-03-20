from django.contrib import admin

# Register your models here.
from .models import Category
from .models import SuggestedCategory

admin.site.register(SuggestedCategory)
admin.site.register(Category)

from django.contrib import admin

# Register your models here.
from .models import Category
from .models import SuggestedCategory


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'description']
    list_filter = ('is_active',)


class SuggestedCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'added_by']
    list_filter = ('added_by',)


admin.site.register(SuggestedCategory, SuggestedCategoryAdmin)
admin.site.register(Category, CategoryAdmin)

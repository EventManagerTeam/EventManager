from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = [
        'event',
        'title',
        'status',
        'is_active',
        'created_at',
        'added_by',
        'assignee',
        'updated_at']
    list_filter = ('status', 'is_active', 'created_at', 'updated_at', 'event')


admin.site.register(Task, TaskAdmin)

from django.contrib import admin

from .models import Event
from .models import Comment
from .models import Invite

class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'country', 'get_categories', 'get_attendees', 'is_active', 'created_at','updated_at']
    list_filter = ('is_active', 'created_at','updated_at', 'added_by', 'country')

    def get_categories(self, obj):
        return ",\n".join([p.name for p in obj.category.all()])

    def get_attendees(self, obj):
        return ",\n".join([p.username for p in obj.attendees.all()])

class CommentAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'event', 'is_active']
    list_filter = ('is_active', 'author', 'event')

    def author(self, obj):
        return obj.added_by.username

class InviteAdmin(admin.ModelAdmin):
    list_display = ['event', 'author','invited', 'is_accepted', 'created_at']
    list_filter = ('is_accepted', 'created_at', 'event')

    def author(self, obj):
        return obj.invited_by.username

    def invited(self, obj):
        return obj.invited_user.username

admin.site.register(Event, EventAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Invite, InviteAdmin)

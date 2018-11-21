from django.contrib import admin

from .models import Event
from .models import Comment


admin.site.register(Event)
admin.site.register(Comment)

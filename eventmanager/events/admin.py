from django.contrib import admin

from .models import Event
from .models import Comment
from .models import Invite


admin.site.register(Event)
admin.site.register(Comment)
admin.site.register(Invite)

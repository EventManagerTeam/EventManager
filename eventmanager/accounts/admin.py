from django.contrib import admin

# Register your models here.
from .models import AccountDetails
from .models import FriendRequest

admin.site.register(AccountDetails)
admin.site.register(FriendRequest)

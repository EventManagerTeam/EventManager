from django.contrib import admin

# Register your models here.
from .models import AccountDetails
from .models import FriendRequest


class AccountDetailsAdmin(admin.ModelAdmin):
    list_display = ['slug', 'get_friends','birth_date','description']

    def get_friends(self, obj):
        return ",\n".join([p.username for p in obj.friends.all()])


class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver']
    list_filter = ('sent_by', 'sent_to')

    def sender(self, obj):
       return str(obj.sent_by)

    def receiver(self, obj):
       return str(obj.sent_to)


admin.site.register(AccountDetails, AccountDetailsAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)

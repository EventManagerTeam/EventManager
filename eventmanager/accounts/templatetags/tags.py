from django import template
from events.models import Invite


register = template.Library()


@register.simple_tag
def number_of_invites(user):
    user_events = Invite.objects.filter(invited_user=user)
    return user_events.filter(is_accepted=False).count()


@register.simple_tag
def has_invites(user):
    if number_of_invites(user) > 0:
        return True
    return False

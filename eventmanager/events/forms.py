from django.forms import ModelForm
from events.models import Event
from events.models import Comment


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = [
            'title',
            'description',
        ]


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [
            'title',
            'content'
        ]

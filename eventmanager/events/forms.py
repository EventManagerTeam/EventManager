from django.forms import ModelForm
from django import forms
from events.models import Event
from events.models import Comment


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'cover_image'
        ]


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [
            'title',
            'content'
        ]

class VisibilitySettings(forms.Form):
    Options = (
            ('1', 'Public'),
            ('2', 'Invited only'),
            ('3', 'Logged users only'),
        )
    visibility = forms.ChoiceField(label='Choose event visibility', widget=forms.Select, choices=Options)
from django import forms
from django.forms import ModelForm

from events.models import Comment
from events.models import Event

from tasks.models import Task


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


class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'status',
            'assignee'
        ]


class VisibilitySettings(forms.Form):
    Options = (
        ('1', 'Public'),
        ('2', 'Logged users only'),
        ('3', 'Invited only'),
    )
    visibility = forms.ChoiceField(
        label='Choose event visibility',
        widget=forms.Select,
        choices=Options)

    class Meta:
        fields = [
            'visibility',
        ]

from django.forms import ModelForm
from events.models import Event


class EventForm(ModelForm):

    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'category',
            'cover_image',
            'starts_at',
            'ends_at'
        ]

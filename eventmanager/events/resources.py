from import_export import resources
from .models import Event


class EventResource(resources.ModelResource):
    class Meta:
        model = Event
        fields = (
            'id',
            'title',
            'description',
            'location',
            'country',
            'starts_at',
            'ends_at')

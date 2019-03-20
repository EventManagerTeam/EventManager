from django import forms
from django.forms import ModelForm

from categories.models import SuggestedCategory


class SuggestedCategoryForm(ModelForm):
    class Meta:
        model = SuggestedCategory
        fields = [
            'name',
            'description',
        ]

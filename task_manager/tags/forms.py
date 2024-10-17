from django import forms
from django.utils.translation import gettext
from task_manager.tags.models import Tag


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = [('name')]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': gettext('Name')}),
        }
        labels = {
            'name': gettext('Name'),
        }

from django import forms
from django.utils.translation import gettext
from task_manager.labels.models import Label


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = [('name')]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': gettext('Name')}),
        }
        labels = {
            'name': gettext('Name'),
        }

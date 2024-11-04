from django import forms
from task_manager.tasks.models import Task
from django.utils.translation import gettext
from django.contrib.auth.models import User


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class TaskForm(forms.ModelForm):
    executor = UserModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        labels = {
            'name': gettext("Name"),
            'description': gettext("Description"),
            'status': gettext("Status"),
            'executor': gettext("Executor"),
            'labels': gettext("Labels"),
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': gettext('Name')}),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 10, 'placeholder': gettext('Description')}),
            'status': forms.Select(
                attrs={
                    'class': 'form-control'}),
            'labels': forms.SelectMultiple(
                attrs={
                    'class': 'form-control', 'size': 4}),
        }

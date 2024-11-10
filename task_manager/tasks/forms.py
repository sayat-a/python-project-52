from django import forms
from task_manager.tasks.models import Task
from django.utils.translation import gettext as _
from task_manager.users.models import CustomUser


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class TaskForm(forms.ModelForm):
    executor = UserModelChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        labels = {
            'name': _("Name"),
            'description': _("Description"),
            'status': _("Status"),
            'executor': _("Executor"),
            'labels': _("Labels"),
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('Name')}),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 10, 'placeholder': _('Description')}),
            'status': forms.Select(
                attrs={
                    'class': 'form-control'}),
            'labels': forms.SelectMultiple(
                attrs={
                    'class': 'form-control', 'size': 4}),
        }

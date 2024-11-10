import django_filters
from django import forms
from task_manager.users.models import CustomUser
from django.forms import widgets
from django.utils.translation import gettext as _
from task_manager.tasks.models import Task
from task_manager.labels.models import Label
from task_manager.statuses.models import Status


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=_("Status"),
        widget=widgets.Select(attrs={'class': 'form-select ml-2 mr-3 mb-3'})
    )

    executor = django_filters.ModelChoiceFilter(
        queryset=CustomUser.objects.all(),
        label=_("Executor"),
        widget=widgets.Select(attrs={'class': 'form-select ml-2 mr-3 mb-3'}),
    )

    label = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_("Label"),
        widget=widgets.Select(attrs={'class': 'form-select ml-2 mr-3 mb-3'}),
        field_name='labels'
    )

    filter_own_tasks = django_filters.BooleanFilter(
        label=_("Only own tasks"),
        method='filter_by_author',
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input mr-3 mb-4'})
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label', 'filter_own_tasks']

    def filter_by_author(self, queryset, name, value):
        if value:
            return queryset.filter(creator=self.request.user)
        return queryset

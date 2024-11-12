from task_manager.statuses.models import Status
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.statuses.forms import StatusForm
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView
)
from task_manager.mixins import DeletionCheckMixin


class StatusListView(ListView):
    model = Status
    template_name = 'statuses/statuses_list.html'
    context_object_name = 'statuses'


class StatusCreateView(SuccessMessageMixin, CreateView):
    model = Status
    template_name = 'statuses/status_form.html'
    form_class = StatusForm
    success_url = reverse_lazy('statuses_list')
    success_message = _("Status is successfully created")


class StatusUpdateView(SuccessMessageMixin, UpdateView):
    model = Status
    template_name = 'statuses/status_form.html'
    form_class = StatusForm
    success_url = reverse_lazy('statuses_list')
    success_message = _("Status is successfully updated")


class StatusDeleteView(SuccessMessageMixin, DeletionCheckMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_delete.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _("Status is successfully deleted")
    error_message = _("Cannot delete status because it is in use")

    def has_dependencies(self, status):
        return status.task_set.exists()

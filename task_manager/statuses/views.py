from task_manager.statuses.models import Status
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.statuses.forms import StatusForm
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView
)


# Create your views here.
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


class StatusDeleteView(SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_delete.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _("Status is successfully deleted")

    def form_valid(self, form):
        if self.get_object().task_set.exists():
            messages.error(
                self.request,
                _("Cannot delete status because it is in use")
            )
            return redirect(self.success_url)
        response = super().form_valid(form)
        return response
